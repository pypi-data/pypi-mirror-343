"""
smol-db - A database system built on top of smol-format for efficient storage and
querying of structured data.
"""

from .core.database import SmolDB
from .core.table import Table
from .core.index import Index

__version__ = "0.1.0"
__all__ = ["SmolDB", "Table", "Index"]