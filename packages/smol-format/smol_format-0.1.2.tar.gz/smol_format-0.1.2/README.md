# smol-format

A high-density data storage system for efficient encoding and decoding of structured data, with special support for large rational numbers.

## Overview

smol-format is a Python library that provides efficient storage and retrieval of structured data, with a particular focus on preserving exact rational numbers of arbitrary size. It combines JSON encoding for data preservation with Zstandard compression to achieve high data density while maintaining exact precision.

Key features:
- Exact preservation of rational numbers (no precision loss)
- Efficient compression with Zstandard
- Simple JSON-based encoding
- Streaming support for large datasets
- Simple API for encoding/decoding
- Metadata tracking
- Type preservation

## Installation

```bash
pip install smol-format
```

## Quick Start

```python
from smol_format import DenseStorage, StorageConfig

# Initialize storage
storage = DenseStorage(
    config=StorageConfig(
        compression_level=3,  # Zstandard compression level (1-22)
        encoding="json"       # Use JSON encoding for data preservation
    )
)

# Example data with large rational numbers
data = {
    "numbers": [1, 2, 3, 4, 5],
    "rationals": [
        "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "271828182845904523536028747135266249775724709369995957496696762772407663035354759457138217852516642/100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
    ]
}

# Encode data
encoded = storage.encode(data)

# Decode data
decoded = storage.decode(encoded)

# Get metadata
metadata = storage.get_metadata(data)
print(metadata)
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

smol-format preserves rational numbers exactly as strings, without any loss of precision:
- No floating-point approximations
- Maintains numerator/denominator format
- Supports arbitrarily large numbers
- Perfect for mathematical applications

### Efficient Compression

Data is compressed using Zstandard, which offers:
- High compression ratios
- Fast compression and decompression
- Configurable compression levels
- Excellent performance on text data

### Streaming Support

For large datasets, smol-format provides streaming capabilities:

```python
# Stream encode
for chunk in data_iterator:
    encoded_chunk = storage.encode(chunk)
    process_encoded_chunk(encoded_chunk)

# Stream decode
for chunk in encoded_chunks:
    decoded_chunk = storage.decode(chunk)
    process_decoded_chunk(decoded_chunk)
```

### Metadata Management

Each dataset includes metadata:
- Number of rows
- Column information
- Data types (with special handling for rationals)
- Creation timestamp

## Use Cases

smol-format is particularly useful for:
- Scientific computing with exact rational arithmetic
- Number theory research
- Cryptography applications
- Any application requiring exact rational number preservation
- General structured data storage

## Examples

Check out the `examples` directory for more detailed examples:
- `rational_numbers.py`: Working with large rational numbers
- `streaming.py`: Handling large datasets with streaming
- `scientific_data.py`: Scientific computing examples

## Performance

smol-format achieves good compression ratios while maintaining exact precision:
- Typical compression ratios: 2-5x for rational number data
- Fast encoding/decoding through JSON
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