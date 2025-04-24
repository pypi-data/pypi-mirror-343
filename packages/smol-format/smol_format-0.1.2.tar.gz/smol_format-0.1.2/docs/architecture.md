# smol-format Architecture

## Design Philosophy

smol-format is designed with a focus on simplicity and exactness. The core principles are:

1. **Exact Preservation**: Rational numbers are stored exactly as strings, maintaining their full precision
2. **Simple Encoding**: JSON is used for human-readable, lossless encoding
3. **Efficient Compression**: Zstandard provides high compression ratios while maintaining speed
4. **Type Awareness**: Metadata tracks data types, especially for rational numbers

## Core Components

### DenseStorage

The main class that handles data storage and retrieval. It provides:

- Encoding/decoding of data
- Compression/decompression
- Metadata generation
- Streaming support

### StorageConfig

Configuration class that controls:

- Compression level (1-22)
- Encoding format (currently only JSON)
- Validation settings
- Chunk size for streaming

## Data Flow

1. **Input Data** → **JSON Encoding** → **Zstandard Compression** → **Storage**
2. **Storage** → **Zstandard Decompression** → **JSON Decoding** → **Output Data**

## Rational Number Handling

Rational numbers are stored as strings in the format "numerator/denominator". This approach:

- Preserves exact values
- Avoids floating-point precision issues
- Allows for arbitrary precision
- Makes it easy to parse and validate

## Compression Strategy

Zstandard is used because it:

- Provides excellent compression ratios for text data
- Has fast compression and decompression speeds
- Supports configurable compression levels
- Is well-maintained and widely used

## Metadata

Each dataset includes metadata about:

- Number of rows
- Column names
- Data types (with special handling for rationals)
- Creation timestamp

## Future Considerations

Potential areas for future development:

1. Support for other encoding formats (e.g., MessagePack)
2. Custom compression algorithms for rational numbers
3. Indexing for faster retrieval
4. Caching mechanisms
5. Parallel processing support