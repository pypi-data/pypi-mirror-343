"""
Index implementation for smol-db.

This module provides the index interface for smol-db, including index creation,
maintenance, and lookup operations. It handles index storage and retrieval
through the storage engine.
"""
from typing import Dict, List, Any, Tuple, Optional, Union
import logging
from pathlib import Path

from ..storage.engine import StorageEngine
from .table import Table

logger = logging.getLogger(__name__)


class Index:
    """Index class for optimizing queries.

    This class provides the interface for index operations including creation,
    maintenance, and lookup. It handles index storage and retrieval through
    the storage engine.

    Attributes:
        table: Table this index belongs to
        columns: List of column names to index
        storage: Storage engine instance
        name: Index name
    """

    def __init__(self, table: Table, columns: List[str], storage: StorageEngine) -> None:
        """Initialize index.

        Args:
            table: Table this index belongs to
            columns: List of column names to index
            storage: Storage engine instance

        Raises:
            ValueError: If columns list is empty
        """
        if not columns:
            raise ValueError("Must specify at least one column to index")

        self.table = table
        self.columns = columns
        self.storage = storage
        self.name = f"{table.name}_{'_'.join(columns)}_index"
        logger.info(f"Initialized index {self.name}")

    def _extract_key(self, data: Dict[str, Any]) -> Tuple[Any, ...]:
        """Extract key values from row data.

        Args:
            data: Row data to extract key from

        Returns:
            Tuple of key values

        Raises:
            ValueError: If required columns are missing
        """
        try:
            return tuple(data[col] for col in self.columns)
        except KeyError as e:
            raise ValueError(f"Missing column for index key: {e}")

    def insert(self, data: Dict[str, Any]) -> None:
        """Insert a row into the index.

        Args:
            data: Row data to index

        Raises:
            ValueError: If required columns are missing
            OSError: If index storage operation fails
        """
        try:
            key = self._extract_key(data)
            self.storage.write_index_entry(self.name, key, data)
            logger.debug(f"Inserted entry into index {self.name}")
        except Exception as e:
            logger.error(f"Failed to insert into index {self.name}: {e}")
            raise

    def lookup(
        self,
        key: Union[Any, Tuple[Any, ...]],
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Lookup rows by key.

        Args:
            key: Key value to look up (single value or tuple for multi-column index)
            limit: Maximum number of rows to return

        Returns:
            List of matching rows

        Raises:
            ValueError: If key format is invalid
            OSError: If index lookup fails
        """
        try:
            # Convert single value to tuple for consistency
            if not isinstance(key, tuple):
                key = (key,)

            if len(key) != len(self.columns):
                raise ValueError(
                    f"Key length {len(key)} does not match index columns {len(self.columns)}"
                )

            results = self.storage.read_index_entries(self.name, key)
            if limit:
                results = results[:limit]

            logger.debug(f"Looked up {len(results)} entries in index {self.name}")
            return results
        except Exception as e:
            logger.error(f"Failed to lookup in index {self.name}: {e}")
            raise

    def drop(self) -> None:
        """Drop the index.

        Raises:
            OSError: If index deletion fails
        """
        try:
            self.storage.drop_index(self.name)
            logger.info(f"Dropped index {self.name}")
        except Exception as e:
            logger.error(f"Failed to drop index {self.name}: {e}")
            raise

    def __enter__(self) -> 'Index':
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        # Add cleanup if needed
        pass