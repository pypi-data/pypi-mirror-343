"""
Tests for smol-db database functionality.
"""
import pytest
import shutil
from pathlib import Path
from typing import Dict, Any

from smol_db import SmolDB, DBConfig


@pytest.fixture
def db_path(tmp_path):
    """Create a temporary database path."""
    path = tmp_path / "test_db"
    path.mkdir()
    yield path
    shutil.rmtree(path)


@pytest.fixture
def db(db_path):
    """Create a test database."""
    return SmolDB(db_path, config=DBConfig(compression_level=1))


def test_database_initialization(db_path: Path, db_config: DBConfig) -> None:
    """Test database initialization."""
    # Test with default config
    db = SmolDB(db_path)
    assert db.path == db_path
    assert db.config.compression_level == 3  # Default value

    # Test with custom config
    db = SmolDB(db_path, config=db_config)
    assert db.path == db_path
    assert db.config.compression_level == db_config.compression_level
    assert db.config.cache_size == db_config.cache_size


def test_database_context_manager(db_path: Path) -> None:
    """Test database context manager."""
    with SmolDB(db_path) as db:
        assert isinstance(db, SmolDB)
        assert db.path == db_path


def test_create_table(db: SmolDB, sample_schema: Dict[str, str]) -> None:
    """Test table creation."""
    # Test successful creation
    table = db.create_table("test", sample_schema)
    assert table.name == "test"
    assert table.schema == sample_schema

    # Test duplicate table
    with pytest.raises(ValueError, match="Table test already exists"):
        db.create_table("test", sample_schema)

    # Test invalid table name
    with pytest.raises(ValueError, match="Table name must be a non-empty string"):
        db.create_table("", sample_schema)

    # Test invalid schema
    with pytest.raises(ValueError, match="Unsupported column type"):
        db.create_table("invalid", {"x": "invalid_type"})


def test_get_table(db: SmolDB, sample_schema: Dict[str, str]) -> None:
    """Test getting a table."""
    # Test non-existent table
    with pytest.raises(ValueError, match="Table test does not exist"):
        db.get_table("test")

    # Test existing table
    table = db.create_table("test", sample_schema)
    retrieved = db.get_table("test")
    assert retrieved == table


def test_list_tables(db: SmolDB, sample_schema: Dict[str, str]) -> None:
    """Test listing tables."""
    assert db.list_tables() == []

    db.create_table("table1", sample_schema)
    db.create_table("table2", sample_schema)

    tables = db.list_tables()
    assert len(tables) == 2
    assert "table1" in tables
    assert "table2" in tables


def test_drop_table(db: SmolDB, sample_schema: Dict[str, str]) -> None:
    """Test dropping a table."""
    # Test non-existent table
    with pytest.raises(ValueError, match="Table test does not exist"):
        db.drop_table("test")

    # Test successful drop
    db.create_table("test", sample_schema)
    assert "test" in db.list_tables()

    db.drop_table("test")
    assert "test" not in db.list_tables()


def test_database_operations(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test database operations."""
    # Create table
    table = db.create_table("test", sample_schema)

    # Insert data
    table.insert(sample_data)

    # Query data
    results = list(table.select())
    assert len(results) == 1
    assert results[0] == sample_data

    # Create index
    index = table.create_index(["curve_id"])
    assert index.name == "test_curve_id_index"

    # Query using index
    results = list(table.select({"curve_id": "E1"}))
    assert len(results) == 1
    assert results[0] == sample_data

    # Drop table
    db.drop_table("test")
    assert "test" not in db.list_tables()


def test_database_error_handling(db: SmolDB) -> None:
    """Test database error handling."""
    # Test invalid path
    with pytest.raises(OSError):
        SmolDB("/invalid/path")

    # Test invalid config
    with pytest.raises(ValueError):
        DBConfig(compression_level=0)  # Invalid compression level

    # Test table operations with invalid data
    table = db.create_table("test", {"x": "string"})

    with pytest.raises(ValueError):
        table.insert({"y": "value"})  # Missing required column

    with pytest.raises(ValueError):
        table.insert({"x": 123})  # Invalid type