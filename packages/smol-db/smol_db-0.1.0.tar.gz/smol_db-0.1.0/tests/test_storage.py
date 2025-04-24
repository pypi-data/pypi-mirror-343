"""
Tests for smol-db storage engine functionality.
"""
import pytest
from pathlib import Path
from typing import Dict, Any
import json

from smol_db import SmolDB, DBConfig
from smol_db.storage.engine import StorageEngine


@pytest.fixture
def storage_path(tmp_path: Path) -> Path:
    """Create a temporary storage path."""
    path = tmp_path / "test_storage"
    path.mkdir()
    return path


@pytest.fixture
def storage_config() -> DBConfig:
    """Create a test storage configuration."""
    return DBConfig(
        data_dir="test_data",
        cache_size=100,
        compression_level=1
    )


@pytest.fixture
def storage(storage_path: Path, storage_config: DBConfig) -> StorageEngine:
    """Create a test storage engine."""
    return StorageEngine(storage_path, storage_config)


def test_storage_initialization(storage_path: Path, storage_config: DBConfig) -> None:
    """Test storage engine initialization."""
    # Test successful creation
    storage = StorageEngine(storage_path, storage_config)
    assert storage.path == storage_path
    assert storage.config == storage_config
    assert storage_path.exists()

    # Test invalid path
    with pytest.raises(OSError):
        StorageEngine(Path("/invalid/path"), storage_config)


def test_storage_context_manager(storage_path: Path, storage_config: DBConfig) -> None:
    """Test storage engine context manager."""
    with StorageEngine(storage_path, storage_config) as storage:
        assert isinstance(storage, StorageEngine)
        assert storage.path == storage_path


def test_write_read_row(storage: StorageEngine, sample_data: Dict[str, Any]) -> None:
    """Test writing and reading rows."""
    # Test single row
    storage.write_row("test_table", sample_data)
    rows = list(storage.read_rows("test_table"))
    assert len(rows) == 1
    assert rows[0] == sample_data

    # Test multiple rows
    data1 = {**sample_data, "curve_id": "E1"}
    data2 = {**sample_data, "curve_id": "E2"}
    storage.write_row("test_table", data1)
    storage.write_row("test_table", data2)

    rows = list(storage.read_rows("test_table"))
    assert len(rows) == 3  # Including the first row

    # Test reading with limit
    rows = list(storage.read_rows("test_table", limit=2))
    assert len(rows) == 2

    # Test reading non-existent table
    rows = list(storage.read_rows("non_existent"))
    assert len(rows) == 0


def test_write_read_index(storage: StorageEngine, sample_data: Dict[str, Any]) -> None:
    """Test writing and reading index entries."""
    # Test single entry
    key = ("E1",)
    storage.write_index_entry("test_index", key, sample_data)
    entries = storage.read_index_entries("test_index", key)
    assert len(entries) == 1
    assert entries[0] == sample_data

    # Test multiple entries with same key
    data1 = {**sample_data, "x": "1/2"}
    data2 = {**sample_data, "x": "3/4"}
    storage.write_index_entry("test_index", key, data1)
    storage.write_index_entry("test_index", key, data2)

    entries = storage.read_index_entries("test_index", key)
    assert len(entries) == 3  # Including the first entry

    # Test reading with limit
    entries = storage.read_index_entries("test_index", key, limit=2)
    assert len(entries) == 2

    # Test reading non-existent index
    entries = storage.read_index_entries("non_existent", key)
    assert len(entries) == 0

    # Test reading non-existent key
    entries = storage.read_index_entries("test_index", ("E2",))
    assert len(entries) == 0


def test_drop_table(storage: StorageEngine, sample_data: Dict[str, Any]) -> None:
    """Test dropping a table."""
    # Write some data
    storage.write_row("test_table", sample_data)
    assert list(storage.read_rows("test_table"))

    # Drop table
    storage.drop_table("test_table")
    assert not list(storage.read_rows("test_table"))

    # Drop non-existent table (should not raise)
    storage.drop_table("non_existent")


def test_drop_index(storage: StorageEngine, sample_data: Dict[str, Any]) -> None:
    """Test dropping an index."""
    # Write some data
    key = ("E1",)
    storage.write_index_entry("test_index", key, sample_data)
    assert storage.read_index_entries("test_index", key)

    # Drop index
    storage.drop_index("test_index")
    assert not storage.read_index_entries("test_index", key)

    # Drop non-existent index (should not raise)
    storage.drop_index("non_existent")


def test_storage_error_handling(storage: StorageEngine) -> None:
    """Test storage engine error handling."""
    # Test invalid JSON data
    class NonSerializable:
        pass

    with pytest.raises(TypeError):
        storage.write_row("test_table", {"data": NonSerializable()})

    # Test invalid file operations
    storage.path.chmod(0o444)  # Make read-only
    with pytest.raises(OSError):
        storage.write_row("test_table", {"x": "1/2"})
    storage.path.chmod(0o777)  # Restore permissions


def test_file_path_handling(storage: StorageEngine) -> None:
    """Test file path handling."""
    # Test table path
    table_path = storage._get_file_path("test_table")
    assert table_path == storage.path / "test_table.smol"

    # Test index path
    index_path = storage._get_file_path("test_index")
    assert index_path == storage.path / "test_index.smol"

    # Test path with special characters
    special_path = storage._get_file_path("test/table")
    assert special_path == storage.path / "test/table.smol"