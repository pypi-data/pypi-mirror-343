# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial development version

### Fixed
- Added smol-format dependency from PyPI

## [0.1.0] - 2025-04-23

### Added
- Initial release of smol-db
- Core database functionality:
  - Table-based data model with schema validation
  - Support for multiple data types including rational numbers
  - Automatic type conversion and validation
- Storage features:
  - Zstandard compression with configurable levels (1-22)
  - Efficient storage format using smol-format
  - Metadata tracking for tables and indexes
- Query capabilities:
  - Basic query interface with filtering
  - Indexing system for fast lookups
  - Support for multiple index types
- Performance features:
  - Streaming support for large datasets
  - Configurable cache size
  - Background processing capabilities
- Development infrastructure:
  - Comprehensive test suite with pytest
  - Code formatting with black and isort
  - Type checking with mypy
  - Linting with flake8
- Documentation:
  - Architecture guide
  - Performance guide
  - API documentation
  - Example code in the examples directory
  - Contributing guidelines
  - Security policy
  - Code of conduct

[Unreleased]: https://github.com/smol-data/smol-db/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/smol-data/smol-db/releases/tag/v0.1.0
