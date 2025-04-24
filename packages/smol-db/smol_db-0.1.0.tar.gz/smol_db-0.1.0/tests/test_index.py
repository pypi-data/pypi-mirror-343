"""
Tests for smol-db index functionality.
"""
import pytest
from typing import Dict, Any, List
from datetime import datetime
from decimal import Decimal

from smol_db import SmolDB


def test_index_initialization(db: SmolDB, sample_schema: Dict[str, str]) -> None:
    """Test index initialization."""
    table = db.create_table("test", sample_schema)

    # Test successful creation
    index = table.create_index(["curve_id"])
    assert index.name == "test_curve_id_index"
    assert index.columns == ["curve_id"]
    assert index.table == table

    # Test multi-column index
    index = table.create_index(["curve_id", "is_valid"])
    assert index.name == "test_curve_id_is_valid_index"
    assert index.columns == ["curve_id", "is_valid"]

    # Test empty columns
    with pytest.raises(ValueError, match="Must specify at least one column"):
        table.create_index([])

    # Test invalid columns
    with pytest.raises(ValueError, match="Columns do not exist"):
        table.create_index(["invalid"])


def test_index_context_manager(db: SmolDB, sample_schema: Dict[str, str]) -> None:
    """Test index context manager."""
    table = db.create_table("test", sample_schema)
    index = table.create_index(["curve_id"])

    with index as i:
        assert i == index


def test_index_key_extraction(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test index key extraction."""
    table = db.create_table("test", sample_schema)
    index = table.create_index(["curve_id"])

    # Test successful extraction
    key = index._extract_key(sample_data)
    assert key == (sample_data["curve_id"],)

    # Test multi-column key
    index = table.create_index(["curve_id", "is_valid"])
    key = index._extract_key(sample_data)
    assert key == (sample_data["curve_id"], sample_data["is_valid"])

    # Test missing column
    with pytest.raises(ValueError, match="Missing column for index key"):
        index._extract_key({"curve_id": "E1"})


def test_index_insert(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test index insertion."""
    table = db.create_table("test", sample_schema)
    index = table.create_index(["curve_id"])

    # Test successful insertion
    index.insert(sample_data)
    results = index.lookup(sample_data["curve_id"])
    assert len(results) == 1
    assert results[0] == sample_data

    # Test missing column
    with pytest.raises(ValueError, match="Missing column for index key"):
        index.insert({"x": "1/2"})


def test_index_lookup(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test index lookup."""
    table = db.create_table("test", sample_schema)
    index = table.create_index(["curve_id"])

    # Insert multiple rows
    data1 = {**sample_data, "curve_id": "E1"}
    data2 = {**sample_data, "curve_id": "E2"}
    index.insert(data1)
    index.insert(data2)

    # Test single key lookup
    results = index.lookup("E1")
    assert len(results) == 1
    assert results[0] == data1

    # Test multi-column key lookup
    index = table.create_index(["curve_id", "is_valid"])
    index.insert(data1)
    results = index.lookup(("E1", True))
    assert len(results) == 1
    assert results[0] == data1

    # Test lookup with limit
    results = index.lookup(("E1", True), limit=1)
    assert len(results) == 1

    # Test lookup with non-existent key
    results = index.lookup(("E3", True))
    assert len(results) == 0

    # Test lookup with invalid key format
    with pytest.raises(ValueError, match="Key length"):
        index.lookup("E1")  # Should be tuple for multi-column index


def test_index_drop(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test dropping an index."""
    table = db.create_table("test", sample_schema)
    index = table.create_index(["curve_id"])

    # Insert data
    index.insert(sample_data)

    # Drop index
    index.drop()

    # Verify data is gone
    results = index.lookup(sample_data["curve_id"])
    assert len(results) == 0


def test_index_error_handling(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test index error handling."""
    table = db.create_table("test", sample_schema)
    index = table.create_index(["curve_id"])

    # Test invalid key format
    with pytest.raises(ValueError, match="Key length"):
        index.lookup(("E1", "extra"))  # Too many components

    # Test missing key column
    with pytest.raises(ValueError, match="Missing column for index key"):
        index.insert({"x": "1/2"})  # Missing curve_id

    # Test invalid key type
    with pytest.raises(ValueError, match="Invalid type"):
        index.insert({**sample_data, "curve_id": 123})  # Should be string