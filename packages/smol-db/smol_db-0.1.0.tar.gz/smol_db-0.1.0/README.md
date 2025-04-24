# smol-db

A database system built on top of smol-format for efficient storage and querying of structured data with exact rational number support.

## Overview

smol-db is a Python library that provides a database-like interface for storing and querying structured data, with a particular focus on preserving exact rational numbers of arbitrary size. It builds on top of smol-format to provide efficient storage while adding database features like indexing and querying.

Key features:
- Exact preservation of rational numbers (no precision loss)
- Efficient compression with Zstandard
- Simple table-based data model
- Indexing for fast lookups
- Streaming support for large datasets
- Simple API for database operations
- Metadata tracking
- Type preservation

## Installation

```bash
pip install smol-db
```

## Quick Start

```python
from smol_db import SmolDB, DBConfig

# Initialize database
db = SmolDB(
    "my_database",
    config=DBConfig(
        compression_level=3,  # Zstandard compression level (1-22)
        cache_size=1000      # Number of rows to cache
    )
)

# Create a table
points_table = db.create_table("points", {
    "x": "rational",
    "y": "rational",
    "curve_id": "string"
})

# Create an index
points_table.create_index(["curve_id"])

# Insert data
points_table.insert({
    "x": "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "y": "271828182845904523536028747135266249775724709369995957496696762772407663035354759457138217852516642/100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "curve_id": "E1"
})

# Query data
for point in points_table.select({"curve_id": "E1"}):
    print(f"Point: ({point['x']}, {point['y']})")
```

## Documentation

- [Architecture](docs/architecture.md) - Design decisions and core components
- [Performance Guide](docs/performance.md) - Best practices and benchmarks
- [Contributing](CONTRIBUTING.md) - How to contribute to the project
- [Changelog](CHANGELOG.md) - Version history and changes
- [Security Policy](SECURITY.md) - Security considerations and reporting
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community guidelines

## Features

### Exact Number Preservation

smol-db preserves rational numbers exactly as strings, without any loss of precision:
- No floating-point approximations
- Maintains numerator/denominator format
- Supports arbitrarily large numbers
- Perfect for mathematical applications

### Efficient Storage

Data is stored using smol-format, which provides:
- High compression ratios
- Fast compression and decompression
- Configurable compression levels
- Excellent performance on text data

### Database Features

smol-db adds database functionality:
- Table-based data model
- Indexing for fast lookups
- Simple query interface
- Type validation
- Metadata tracking

### Streaming Support

For large datasets, smol-db provides streaming capabilities:
- Process data in chunks
- Memory-efficient operations
- Background processing
- Progress tracking

## Use Cases

smol-db is particularly useful for:
- Scientific computing with exact rational arithmetic
- Number theory research
- Cryptography applications
- Any application requiring exact rational number preservation
- General structured data storage

## Examples

Check out the `examples` directory for more detailed examples:
- `basic_usage.py`: Basic database operations
- `indexing.py`: Working with indexes
- `streaming.py`: Handling large datasets

## Performance

smol-db achieves good performance while maintaining exact precision:
- Typical compression ratios: 2-5x for rational number data
- Fast indexing for lookups
- Efficient streaming for large datasets

See the [Performance Guide](docs/performance.md) for detailed benchmarks and optimization tips.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

Please report any security vulnerabilities to small.joshua@gmail.com. See our [Security Policy](SECURITY.md) for more details.

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.