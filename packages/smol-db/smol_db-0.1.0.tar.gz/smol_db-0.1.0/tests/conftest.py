"""
Test configuration and fixtures for smol-db.
"""
import pytest
import shutil
from pathlib import Path
from typing import Generator, Dict, Any

from smol_db import SmolDB, DBConfig


@pytest.fixture
def db_path(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary database path.

    Args:
        tmp_path: pytest temporary path fixture

    Yields:
        Path to temporary database directory
    """
    path = tmp_path / "test_db"
    path.mkdir()
    yield path
    shutil.rmtree(path)


@pytest.fixture
def db_config() -> DBConfig:
    """Create a test database configuration.

    Returns:
        Database configuration with test settings
    """
    return DBConfig(
        data_dir="test_data",
        cache_size=100,
        compression_level=1
    )


@pytest.fixture
def db(db_path: Path, db_config: DBConfig) -> Generator[SmolDB, None, None]:
    """Create a test database.

    Args:
        db_path: Path to database directory
        db_config: Database configuration

    Yields:
        Database instance
    """
    db = SmolDB(db_path, config=db_config)
    yield db
    # Cleanup is handled by db_path fixture


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """Create sample data for testing.

    Returns:
        Dictionary of sample data
    """
    return {
        "x": "355/113",
        "y": "22/7",
        "curve_id": "E1",
        "timestamp": "2025-04-23T12:00:00",
        "is_valid": True,
        "metadata": {"version": 1, "source": "test"}
    }


@pytest.fixture
def sample_schema() -> Dict[str, str]:
    """Create sample schema for testing.

    Returns:
        Dictionary of column names to types
    """
    return {
        "x": "rational",
        "y": "rational",
        "curve_id": "string",
        "timestamp": "datetime",
        "is_valid": "boolean",
        "metadata": "json"
    }