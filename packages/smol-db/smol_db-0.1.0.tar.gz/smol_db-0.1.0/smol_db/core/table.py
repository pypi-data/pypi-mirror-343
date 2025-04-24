"""
Table implementation for smol-db.

This module provides the table interface for smol-db, including data insertion,
querying, and index management. It handles data validation, storage, and retrieval
operations.
"""
from typing import Dict, List, Any, Iterator, Optional, Set, Union
import logging
from datetime import datetime
from decimal import Decimal
import json

from ..storage.engine import StorageEngine
from .index import Index

logger = logging.getLogger(__name__)


class Table:
    """Table class for storing and querying data.

    This class provides the interface for table operations including data insertion,
    querying, and index management. It handles data validation and coordinates with
    the storage engine for persistence.

    Attributes:
        name: Table name
        schema: Column name to type mapping
        storage: Storage engine instance
        indexes: Dictionary of index names to Index instances
    """

    SUPPORTED_TYPES = {
        'string': str,
        'integer': int,
        'float': float,
        'boolean': bool,
        'datetime': datetime,
        'decimal': Decimal,
        'json': dict
    }

    def __init__(self, name: str, schema: Dict[str, str], storage: StorageEngine) -> None:
        """Initialize table.

        Args:
            name: Table name
            schema: Column name to type mapping
            storage: Storage engine instance

        Raises:
            ValueError: If schema contains invalid types
        """
        if not name or not isinstance(name, str):
            raise ValueError("Table name must be a non-empty string")

        for col_type in schema.values():
            if col_type not in self.SUPPORTED_TYPES:
                raise ValueError(f"Unsupported column type: {col_type}")

        self.name = name
        self.schema = schema
        self.storage = storage
        self.indexes: Dict[str, Index] = {}
        logger.info(f"Initialized table {name}")

    def _validate_data(self, data: Dict[str, Any]) -> None:
        """Validate data against schema.

        Args:
            data: Row data to validate

        Raises:
            ValueError: If data doesn't match schema
        """
        # Check all required columns are present
        missing_cols = set(self.schema.keys()) - set(data.keys())
        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")

        # Validate data types
        for col, value in data.items():
            if col not in self.schema:
                raise ValueError(f"Unexpected column: {col}")

            expected_type = self.SUPPORTED_TYPES[self.schema[col]]
            if not isinstance(value, expected_type):
                raise ValueError(
                    f"Invalid type for column {col}: expected {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )

    def insert(self, data: Dict[str, Any]) -> None:
        """Insert a row into the table.

        Args:
            data: Row data matching schema

        Raises:
            ValueError: If data doesn't match schema
            OSError: If storage operation fails
        """
        try:
            self._validate_data(data)
            self.storage.write_row(self.name, data)

            # Update indexes
            for index in self.indexes.values():
                index.insert(data)

            logger.debug(f"Inserted row into table {self.name}")
        except Exception as e:
            logger.error(f"Failed to insert row into table {self.name}: {e}")
            raise

    def select(
        self,
        conditions: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None
    ) -> Iterator[Dict[str, Any]]:
        """Select rows matching conditions.

        Args:
            conditions: Column to value mapping for filtering
            limit: Maximum number of rows to return

        Returns:
            Iterator of matching rows

        Raises:
            ValueError: If conditions contain invalid columns
        """
        if conditions:
            invalid_cols = set(conditions.keys()) - set(self.schema.keys())
            if invalid_cols:
                raise ValueError(f"Invalid columns in conditions: {invalid_cols}")

        try:
            count = 0
            for row in self.storage.read_rows(self.name):
                if conditions is None or all(
                    row.get(k) == v for k, v in conditions.items()
                ):
                    yield row
                    count += 1
                    if limit and count >= limit:
                        break
        except Exception as e:
            logger.error(f"Failed to select rows from table {self.name}: {e}")
            raise

    def create_index(self, columns: List[str]) -> Index:
        """Create an index on columns.

        Args:
            columns: List of column names to index

        Returns:
            Created index

        Raises:
            ValueError: If columns don't exist
            OSError: If index creation fails
        """
        if not columns:
            raise ValueError("Must specify at least one column to index")

        # Validate columns
        invalid_cols = set(columns) - set(self.schema.keys())
        if invalid_cols:
            raise ValueError(f"Columns do not exist: {invalid_cols}")

        try:
            # Create index
            index_name = "_".join(columns)
            index = Index(self, columns, self.storage)
            self.indexes[index_name] = index
            logger.info(f"Created index {index_name} on table {self.name}")
            return index
        except Exception as e:
            logger.error(f"Failed to create index on table {self.name}: {e}")
            raise

    def drop(self) -> None:
        """Drop the table and all its indexes.

        Raises:
            OSError: If table or index deletion fails
        """
        try:
            self.storage.drop_table(self.name)
            for index in self.indexes.values():
                index.drop()
            self.indexes.clear()
            logger.info(f"Dropped table {self.name}")
        except Exception as e:
            logger.error(f"Failed to drop table {self.name}: {e}")
            raise

    def __enter__(self) -> 'Table':
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        # Add cleanup if needed
        pass