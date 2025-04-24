"""
Core database implementation for smol-db.

This module provides the main database interface for smol-db, including table management
and configuration. It handles the creation, retrieval, and deletion of tables, as well
as database-wide configuration.
"""
from typing import Dict, Optional, List, Any
from pathlib import Path
import logging
from pydantic import BaseModel, Field, validator

from ..storage.engine import StorageEngine
from .table import Table

logger = logging.getLogger(__name__)


class DBConfig(BaseModel):
    """Database configuration.

    Attributes:
        data_dir: Directory where database files are stored
        cache_size: Number of rows to keep in memory cache
        compression_level: Zstandard compression level (1-22)
    """
    data_dir: str = Field(
        default="data",
        description="Database data directory"
    )
    cache_size: int = Field(
        default=1000,
        ge=1,
        description="Number of rows to cache"
    )
    compression_level: int = Field(
        default=3,
        ge=1,
        le=22,
        description="Zstandard compression level"
    )

    @validator('compression_level')
    def validate_compression_level(cls, v: int) -> int:
        """Validate compression level is within valid range."""
        if not 1 <= v <= 22:
            raise ValueError("Compression level must be between 1 and 22")
        return v


class SmolDB:
    """Main database class.

    This class provides the primary interface for interacting with the database.
    It manages tables and handles database-wide operations.

    Attributes:
        path: Path to database directory
        config: Database configuration
        storage: Storage engine instance
        tables: Dictionary of table names to Table instances
    """

    def __init__(self, path: str, config: Optional[DBConfig] = None) -> None:
        """Initialize database.

        Args:
            path: Path to database directory
            config: Database configuration

        Raises:
            ValueError: If path is invalid or inaccessible
            OSError: If database directory cannot be created
        """
        try:
            self.path = Path(path)
            self.config = config or DBConfig()
            self.storage = StorageEngine(self.path, self.config)
            self.tables: Dict[str, Table] = {}
            logger.info(f"Initialized database at {self.path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def create_table(self, name: str, schema: Dict[str, str]) -> Table:
        """Create a new table.

        Args:
            name: Table name
            schema: Column name to type mapping

        Returns:
            Created table

        Raises:
            ValueError: If table already exists or schema is invalid
            OSError: If table storage cannot be created
        """
        if not name or not isinstance(name, str):
            raise ValueError("Table name must be a non-empty string")

        if name in self.tables:
            raise ValueError(f"Table {name} already exists")

        try:
            table = Table(name, schema, self.storage)
            self.tables[name] = table
            logger.info(f"Created table {name}")
            return table
        except Exception as e:
            logger.error(f"Failed to create table {name}: {e}")
            raise

    def get_table(self, name: str) -> Table:
        """Get existing table.

        Args:
            name: Table name

        Returns:
            Table instance

        Raises:
            ValueError: If table doesn't exist
        """
        if name not in self.tables:
            raise ValueError(f"Table {name} does not exist")
        return self.tables[name]

    def list_tables(self) -> List[str]:
        """List all tables.

        Returns:
            List of table names
        """
        return list(self.tables.keys())

    def drop_table(self, name: str) -> None:
        """Drop a table.

        Args:
            name: Table name

        Raises:
            ValueError: If table doesn't exist
            OSError: If table storage cannot be deleted
        """
        if name not in self.tables:
            raise ValueError(f"Table {name} does not exist")

        try:
            self.tables[name].drop()
            del self.tables[name]
            logger.info(f"Dropped table {name}")
        except Exception as e:
            logger.error(f"Failed to drop table {name}: {e}")
            raise

    def __enter__(self) -> 'SmolDB':
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        # Add cleanup if needed
        pass
