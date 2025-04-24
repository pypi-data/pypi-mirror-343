"""
Tests for smol-db table functionality.
"""
import pytest
from typing import Dict, Any, List
from datetime import datetime
from decimal import Decimal

from smol_db import SmolDB


def test_table_initialization(db: SmolDB, sample_schema: Dict[str, str]) -> None:
    """Test table initialization."""
    # Test successful creation
    table = db.create_table("test", sample_schema)
    assert table.name == "test"
    assert table.schema == sample_schema
    assert len(table.indexes) == 0

    # Test invalid table name
    with pytest.raises(ValueError, match="Table name must be a non-empty string"):
        db.create_table("", sample_schema)

    # Test invalid schema
    with pytest.raises(ValueError, match="Unsupported column type"):
        db.create_table("invalid", {"x": "invalid_type"})


def test_table_context_manager(db: SmolDB, sample_schema: Dict[str, str]) -> None:
    """Test table context manager."""
    table = db.create_table("test", sample_schema)
    with table as t:
        assert t == table


def test_insert_data(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test data insertion."""
    table = db.create_table("test", sample_schema)

    # Test successful insertion
    table.insert(sample_data)
    results = list(table.select())
    assert len(results) == 1
    assert results[0] == sample_data

    # Test missing columns
    with pytest.raises(ValueError, match="Missing columns"):
        table.insert({"x": "1/2"})

    # Test invalid types
    with pytest.raises(ValueError, match="Invalid type"):
        table.insert({**sample_data, "x": 123})

    # Test extra columns
    with pytest.raises(ValueError, match="Unexpected column"):
        table.insert({**sample_data, "extra": "value"})


def test_select_data(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test data selection."""
    table = db.create_table("test", sample_schema)

    # Insert multiple rows
    data1 = {**sample_data, "curve_id": "E1"}
    data2 = {**sample_data, "curve_id": "E2"}
    table.insert(data1)
    table.insert(data2)

    # Test select all
    results = list(table.select())
    assert len(results) == 2

    # Test select with conditions
    results = list(table.select({"curve_id": "E1"}))
    assert len(results) == 1
    assert results[0] == data1

    # Test select with limit
    results = list(table.select(limit=1))
    assert len(results) == 1

    # Test select with invalid conditions
    with pytest.raises(ValueError, match="Invalid columns in conditions"):
        list(table.select({"invalid": "value"}))


def test_create_index(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test index creation."""
    table = db.create_table("test", sample_schema)

    # Test successful index creation
    index = table.create_index(["curve_id"])
    assert index.name == "test_curve_id_index"
    assert len(table.indexes) == 1

    # Test duplicate index
    with pytest.raises(ValueError, match="Index already exists"):
        table.create_index(["curve_id"])

    # Test invalid columns
    with pytest.raises(ValueError, match="Columns do not exist"):
        table.create_index(["invalid"])

    # Test empty columns
    with pytest.raises(ValueError, match="Must specify at least one column"):
        table.create_index([])

    # Test multi-column index
    index = table.create_index(["curve_id", "is_valid"])
    assert index.name == "test_curve_id_is_valid_index"
    assert len(table.indexes) == 2


def test_index_operations(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test index operations."""
    table = db.create_table("test", sample_schema)

    # Create index
    index = table.create_index(["curve_id"])

    # Insert data
    table.insert(sample_data)

    # Test index lookup
    results = index.lookup("E1")
    assert len(results) == 1
    assert results[0] == sample_data

    # Test index lookup with limit
    results = index.lookup("E1", limit=1)
    assert len(results) == 1

    # Test index lookup with invalid key
    with pytest.raises(ValueError, match="Key length"):
        index.lookup(("E1", "extra"))


def test_drop_table(db: SmolDB, sample_schema: Dict[str, str], sample_data: Dict[str, Any]) -> None:
    """Test dropping a table."""
    table = db.create_table("test", sample_schema)

    # Create index
    index = table.create_index(["curve_id"])

    # Insert data
    table.insert(sample_data)

    # Drop table
    table.drop()
    assert len(table.indexes) == 0

    # Verify data is gone
    results = list(table.select())
    assert len(results) == 0


def test_table_error_handling(db: SmolDB, sample_schema: Dict[str, str]) -> None:
    """Test table error handling."""
    table = db.create_table("test", sample_schema)

    # Test invalid data types
    with pytest.raises(ValueError):
        table.insert({**sample_schema, "x": "invalid"})

    # Test invalid index operations
    with pytest.raises(ValueError):
        table.create_index(["invalid"])

    # Test invalid select conditions
    with pytest.raises(ValueError):
        list(table.select({"invalid": "value"}))
