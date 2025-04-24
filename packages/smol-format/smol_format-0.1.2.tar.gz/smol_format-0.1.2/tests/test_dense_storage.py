"""
Tests for smol-format's DenseStorage implementation.
"""
import pytest
from smol_format import DenseStorage, StorageConfig

def test_basic_encoding_decoding():
    """Test basic encoding and decoding of data."""
    storage = DenseStorage(
        config=StorageConfig(
            compression_level=3,
            encoding="json"
        )
    )

    # Test with simple data
    data = {
        "numbers": [1, 2, 3, 4, 5],
        "strings": ["hello", "world"],
        "floats": [1.23, 4.56, 7.89]
    }

    encoded = storage.encode(data)
    decoded = storage.decode(encoded)

    assert decoded == data

def test_rational_number_preservation():
    """Test that rational numbers are preserved exactly."""
    storage = DenseStorage(
        config=StorageConfig(
            compression_level=3,
            encoding="json"
        )
    )

    # Test with rational numbers
    data = {
        "rationals": [
            "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "271828182845904523536028747135266249775724709369995957496696762772407663035354759457138217852516642/100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        ]
    }

    encoded = storage.encode(data)
    decoded = storage.decode(encoded)

    assert decoded == data
    assert decoded["rationals"][0] == data["rationals"][0]
    assert decoded["rationals"][1] == data["rationals"][1]

def test_metadata_generation():
    """Test metadata generation for different data types."""
    storage = DenseStorage(
        config=StorageConfig(
            compression_level=3,
            encoding="json"
        )
    )

    # Test with mixed data types
    data = {
        "integers": [1, 2, 3],
        "rationals": ["1/2", "3/4", "5/6"],
        "floats": [1.23, 4.56, 7.89],
        "strings": ["hello", "world"]
    }

    metadata = storage.get_metadata(data)

    assert metadata["num_rows"] == 3
    assert set(metadata["columns"]) == {"integers", "rationals", "floats", "strings"}
    assert metadata["data_types"]["integers"] == "int"
    assert metadata["data_types"]["rationals"] == "rational"
    assert metadata["data_types"]["floats"] == "float"
    assert metadata["data_types"]["strings"] == "str"

def test_streaming():
    """Test streaming encoding and decoding."""
    storage = DenseStorage(
        config=StorageConfig(
            compression_level=3,
            encoding="json"
        )
    )

    # Generate test data
    chunks = [
        {"rationals": [f"{i}/{i+1}" for i in range(1000)]}
        for _ in range(5)
    ]

    # Stream encode
    encoded_chunks = [storage.encode(chunk) for chunk in chunks]

    # Stream decode
    decoded_chunks = [storage.decode(chunk) for chunk in encoded_chunks]

    # Verify
    for original, decoded in zip(chunks, decoded_chunks):
        assert original == decoded

def test_compression_levels():
    """Test different compression levels."""
    data = {
        "rationals": [
            "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "271828182845904523536028747135266249775724709369995957496696762772407663035354759457138217852516642/100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        ]
    }

    # Test different compression levels
    for level in [1, 3, 9, 22]:
        storage = DenseStorage(
            config=StorageConfig(
                compression_level=level,
                encoding="json"
            )
        )

        encoded = storage.encode(data)
        decoded = storage.decode(encoded)

        assert decoded == data