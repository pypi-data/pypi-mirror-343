"""
smol-format - A high-density data storage system for efficient encoding and decoding of structured data.
"""

from .core import (
    DenseStorage,
    StorageConfig
)

__version__ = "0.1.1"
__all__ = ["DenseStorage", "StorageConfig"]