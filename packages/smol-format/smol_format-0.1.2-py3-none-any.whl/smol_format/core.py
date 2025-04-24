"""
Core functionality for smol-format data storage.
"""
from typing import Any, Dict, List, Optional, Union, Iterator
import logging
from datetime import datetime
import json
import zstandard as zstd
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class StorageConfig(BaseModel):
    """Configuration for storage."""
    compression_level: int = Field(default=3, ge=1, le=22)
    encoding: str = Field(default="json", pattern="^(json|msgpack)$")
    chunk_size: int = Field(default=10000)
    validate_data: bool = Field(default=True)

class DenseStorage:
    """High-density data storage system."""

    def __init__(self, config: Optional[StorageConfig] = None):
        """
        Initialize storage.

        Args:
            config: Storage configuration
        """
        self.config = config or StorageConfig()
        self.compressor = zstd.ZstdCompressor(level=self.config.compression_level)
        self.decompressor = zstd.ZstdDecompressor()

    def encode(self, data: Union[Dict, List]) -> bytes:
        """
        Encode data to compressed binary format.

        Args:
            data: Input data (dict or list)

        Returns:
            Compressed binary data

        Raises:
            ValueError: If data type is not supported
        """
        try:
            # Convert to JSON string
            json_str = json.dumps(data)

            # Compress
            return self.compressor.compress(json_str.encode('utf-8'))

        except Exception as e:
            logger.error(f"Failed to encode data: {e}")
            raise

    def decode(self, data: bytes) -> Union[Dict, List]:
        """
        Decode compressed binary data.

        Args:
            data: Compressed binary data

        Returns:
            Decoded data as dict or list

        Raises:
            ValueError: If data cannot be decoded
        """
        try:
            # Decompress
            decompressed = self.decompressor.decompress(data)

            # Parse JSON
            return json.loads(decompressed.decode('utf-8'))

        except Exception as e:
            logger.error(f"Failed to decode data: {e}")
            raise

    def get_metadata(self, data: Union[Dict, List]) -> Dict[str, Any]:
        """
        Get metadata about the data.

        Args:
            data: Input data

        Returns:
            Dictionary of metadata
        """
        if isinstance(data, dict):
            return {
                "num_rows": len(next(iter(data.values()))) if data else 0,
                "columns": list(data.keys()),
                "created_at": datetime.now().isoformat(),
                "data_types": {
                    k: "rational" if isinstance(v[0], str) and '/' in v[0] else type(v[0]).__name__
                    for k, v in data.items()
                }
            }
        elif isinstance(data, list):
            return {
                "num_rows": len(data),
                "created_at": datetime.now().isoformat()
            }
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def stream_encode(self, data_iterator: Iterator[Union[Dict, List]]) -> Iterator[bytes]:
        """
        Stream encode data in chunks.

        Args:
            data_iterator: Iterator of data chunks

        Yields:
            Compressed binary chunks
        """
        chunk = []
        for item in data_iterator:
            chunk.append(item)
            if len(chunk) >= self.config.chunk_size:
                yield self.encode(chunk)
                chunk = []
        if chunk:
            yield self.encode(chunk)

    def stream_decode(self, data_iterator: Iterator[bytes]) -> Iterator[Union[Dict, List]]:
        """
        Stream decode compressed data.

        Args:
            data_iterator: Iterator of compressed binary chunks

        Yields:
            Decoded data chunks
        """
        for chunk in data_iterator:
            yield self.decode(chunk)