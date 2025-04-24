"""Basic usage examples for smol-format."""
from smol_format import SmolWriter, SmolReader, SmolStorage
from smol_format.core import (
    COMPRESSION_NONE,
    COMPRESSION_ZLIB,
    COMPRESSION_LZ4,
    COMPRESSION_ZSTD
)


def basic_write_read():
    """Basic write and read operations."""
    # Write points
    with SmolWriter("points.smol") as writer:
        writer.add_point("123/456", "789/101")
        writer.add_point("202/303", "404/505")

    # Read points
    with SmolReader("points.smol") as reader:
        for x, y in reader.read_points():
            print(f"Point: ({x}, {y})")


def compression_examples():
    """Examples of different compression options."""
    # No compression
    with SmolWriter("points_none.smol", compression_type=COMPRESSION_NONE) as writer:
        writer.add_point("123/456", "789/101")

    # Zlib compression
    with SmolWriter("points_zlib.smol", compression_type=COMPRESSION_ZLIB) as writer:
        writer.add_point("123/456", "789/101")

    # LZ4 compression
    with SmolWriter("points_lz4.smol", compression_type=COMPRESSION_LZ4) as writer:
        writer.add_point("123/456", "789/101")

    # Zstandard compression
    with SmolWriter("points_zstd.smol", compression_type=COMPRESSION_ZSTD) as writer:
        writer.add_point("123/456", "789/101")


def storage_examples():
    """Examples of storage operations."""
    # Create storage
    storage = SmolStorage("data_dir")

    # Write points with metadata
    points = [("123/456", "789/101"), ("202/303", "404/505")]
    storage.write_points(
        "curve1",
        points,
        additional_info={
            "description": "Sample curve",
            "author": "John Doe",
            "date": "2025-01-01"
        }
    )

    # Read points
    read_points = list(storage.read_points("curve1"))
    print(f"Read {len(read_points)} points")

    # Get metadata
    metadata = storage.get_metadata("curve1")
    print(f"Curve: {metadata.curve_id}")
    print(f"Points: {metadata.num_points}")
    print(f"Created: {metadata.created_at}")
    print(f"Additional info: {metadata.additional_info}")

    # List files
    files = storage.list_files()
    print(f"Available files: {files}")


def memory_mapping_example():
    """Example of memory mapping for large files."""
    # Write a large number of points
    with SmolWriter("large_points.smol") as writer:
        for i in range(1000000):
            writer.add_point(f"{i}/1", f"{i*2}/1")

    # Read with memory mapping
    with SmolReader("large_points.smol") as reader:
        # This will be faster for large files
        for x, y in reader.read_points(use_mmap=True):
            pass


"""
Basic usage example for smol-db.
"""
from smol_db import SmolDB, DBConfig


def main():
    # Initialize database
    db = SmolDB("example_db", config=DBConfig(compression_level=3))

    # Create a table for storing points
    points_table = db.create_table("points", {
        "x": "rational",
        "y": "rational",
        "curve_id": "string"
    })

    # Create an index on curve_id
    points_table.create_index(["curve_id"])

    # Insert some points
    points = [
        {
            "x": "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "y": "271828182845904523536028747135266249775724709369995957496696762772407663035354759457138217852516642/100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "curve_id": "E1"
        },
        {
            "x": "355/113",
            "y": "22/7",
            "curve_id": "E2"
        }
    ]

    for point in points:
        points_table.insert(point)

    # Query points on curve E1
    print("Points on curve E1:")
    for point in points_table.select({"curve_id": "E1"}):
        print(f"x: {point['x']}")
        print(f"y: {point['y']}")
        print()


if __name__ == "__main__":
    print("Running basic examples...")
    basic_write_read()

    print("\nRunning compression examples...")
    compression_examples()

    print("\nRunning storage examples...")
    storage_examples()

    print("\nRunning memory mapping example...")
    memory_mapping_example()

    main()
