"""
Storage engine implementation using smol-format.

This module provides the storage engine interface for smol-db, handling the
persistence of tables and indexes using smol-format for efficient storage
and compression.
"""
from typing import Dict, List, Any, Iterator, Optional, Union
import logging
from pathlib import Path
import json
import os

from smol_format import DenseStorage, StorageConfig

logger = logging.getLogger(__name__)


class StorageEngine:
    """Storage engine using smol-format.

    This class provides the interface for storage operations including reading
    and writing tables and indexes. It uses smol-format for efficient storage
    and compression.

    Attributes:
        path: Path to storage directory
        config: Database configuration
        storage: smol-format storage instance
    """

    def __init__(self, path: Path, config: Any) -> None:
        """Initialize storage engine.

        Args:
            path: Path to storage directory
            config: Database configuration

        Raises:
            ValueError: If path is invalid
            OSError: If storage directory cannot be created
        """
        try:
            self.path = Path(path)
            self.config = config

            # Create storage directory if it doesn't exist
            self.path.mkdir(parents=True, exist_ok=True)

            self.storage = DenseStorage(
                config=StorageConfig(
                    compression_level=config.compression_level,
                    encoding="json"
                )
            )
            logger.info(f"Initialized storage engine at {self.path}")
        except Exception as e:
            logger.error(f"Failed to initialize storage engine: {e}")
            raise

    def _get_file_path(self, name: str) -> Path:
        """Get file path for a table or index.

        Args:
            name: Name of table or index

        Returns:
            Path to storage file
        """
        return self.path / f"{name}.smol"

    def write_row(self, table_name: str, data: Dict[str, Any]) -> None:
        """Write a row to storage.

        Args:
            table_name: Name of table
            data: Row data to write

        Raises:
            ValueError: If data is invalid
            OSError: If write operation fails
        """
        try:
            # Validate data is JSON serializable
            json.dumps(data)

            self.storage.write_data(table_name, data, file_index=0)
            logger.debug(f"Wrote row to table {table_name}")
        except Exception as e:
            logger.error(f"Failed to write row to table {table_name}: {e}")
            raise

    def read_rows(
        self,
        table_name: str,
        limit: Optional[int] = None
    ) -> Iterator[Dict[str, Any]]:
        """Read rows from storage.

        Args:
            table_name: Name of table
            limit: Maximum number of rows to return

        Yields:
            Row data

        Raises:
            OSError: If read operation fails
        """
        try:
            table_path = self._get_file_path(table_name)
            if not table_path.exists():
                logger.warning(f"Table {table_name} does not exist")
                return

            data = self.storage.read_data(table_name, file_index=0)
            count = 0

            if isinstance(data, list):
                for row in data:
                    yield row
                    count += 1
                    if limit and count >= limit:
                        break
            else:
                yield data

            logger.debug(f"Read {count} rows from table {table_name}")
        except Exception as e:
            logger.error(f"Failed to read rows from table {table_name}: {e}")
            raise

    def write_index_entry(
        self,
        index_name: str,
        key: Union[Any, tuple],
        data: Dict[str, Any]
    ) -> None:
        """Write an index entry.

        Args:
            index_name: Name of index
            key: Index key
            data: Row data

        Raises:
            ValueError: If data is invalid
            OSError: If write operation fails
        """
        try:
            # Validate data is JSON serializable
            json.dumps({"key": key, "data": data})

            self.storage.write_data(
                index_name, {"key": key, "data": data}, file_index=0
            )
            logger.debug(f"Wrote entry to index {index_name}")
        except Exception as e:
            logger.error(f"Failed to write entry to index {index_name}: {e}")
            raise

    def read_index_entries(
        self,
        index_name: str,
        key: Union[Any, tuple],
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Read index entries.

        Args:
            index_name: Name of index
            key: Key to look up
            limit: Maximum number of entries to return

        Returns:
            List of matching rows

        Raises:
            OSError: If read operation fails
        """
        try:
            index_path = self._get_file_path(index_name)
            if not index_path.exists():
                logger.warning(f"Index {index_name} does not exist")
                return []

            data = self.storage.read_data(index_name, file_index=0)
            results = []

            if isinstance(data, list):
                for entry in data:
                    if entry["key"] == key:
                        results.append(entry["data"])
                        if limit and len(results) >= limit:
                            break

            logger.debug(f"Read {len(results)} entries from index {index_name}")
            return results
        except Exception as e:
            logger.error(f"Failed to read entries from index {index_name}: {e}")
            raise

    def drop_table(self, table_name: str) -> None:
        """Drop a table.

        Args:
            table_name: Name of table

        Raises:
            OSError: If deletion fails
        """
        try:
            table_path = self._get_file_path(table_name)
            if table_path.exists():
                table_path.unlink()
                logger.info(f"Dropped table {table_name}")
        except Exception as e:
            logger.error(f"Failed to drop table {table_name}: {e}")
            raise

    def drop_index(self, index_name: str) -> None:
        """Drop an index.

        Args:
            index_name: Name of index

        Raises:
            OSError: If deletion fails
        """
        try:
            index_path = self._get_file_path(index_name)
            if index_path.exists():
                index_path.unlink()
                logger.info(f"Dropped index {index_name}")
        except Exception as e:
            logger.error(f"Failed to drop index {index_name}: {e}")
            raise

    def __enter__(self) -> 'StorageEngine':
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        # Add cleanup if needed
        pass