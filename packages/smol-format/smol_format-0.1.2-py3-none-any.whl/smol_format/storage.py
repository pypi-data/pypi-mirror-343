"""
Storage management for smol-format files.
"""
from pathlib import Path
from typing import List, Tuple, Iterator, Optional, Dict, Any, Union
import logging
from datetime import datetime
import json
import shutil
from dataclasses import dataclass, asdict

from .core import DenseStorage, StorageConfig

logger = logging.getLogger(__name__)

@dataclass
class SmolMetadata:
    """Metadata for smol-format files."""
    curve_id: str
    file_index: int
    created_at: datetime
    num_points: int
    coord_bits: int
    compression_type: int
    field_types: Dict[str, str]  # Maps field names to their types
    additional_info: Dict[str, Any] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        data = asdict(self)
        data['created_at'] = data['created_at'].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SmolMetadata':
        """Create metadata from dictionary."""
        data = data.copy()
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        return cls(**data)

class SmolStorage:
    """Manages storage of data using smol-format files."""

    def __init__(
        self,
        data_dir: str = "smol_data",
        config: Optional[StorageConfig] = None,
        metadata_dir: Optional[str] = None
    ):
        """
        Initialize storage.

        Args:
            data_dir: Directory for smol-format files
            config: Storage configuration
            metadata_dir: Directory for metadata files (defaults to data_dir)
        """
        self.data_dir = Path(data_dir)
        self.config = config or StorageConfig()
        self.metadata_dir = Path(metadata_dir) if metadata_dir else self.data_dir
        self.storage = DenseStorage(config=self.config)

        # Create directories
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def _get_metadata_path(self, data_id: str, file_index: int) -> Path:
        """Get path for metadata file."""
        return self.metadata_dir / f"{data_id}_{file_index:03d}.json"

    def _save_metadata(self, data_id: str, file_index: int, metadata: Dict[str, Any]) -> None:
        """Save metadata to file."""
        try:
            metadata_path = self._get_metadata_path(data_id, file_index)
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
            raise

    def _load_metadata(self, data_id: str, file_index: int) -> Optional[Dict[str, Any]]:
        """Load metadata from file."""
        try:
            metadata_path = self._get_metadata_path(data_id, file_index)
            if not metadata_path.exists():
                return None

            with open(metadata_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load metadata: {e}")
            raise

    def write_data(
        self,
        data_id: str,
        data: Union[Dict, List, Any],
        file_index: int = 0,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Write data to a smol-format file.

        Args:
            data_id: Data identifier
            data: Data to write
            file_index: Index for the file name
            additional_info: Additional metadata to store

        Raises:
            ValueError: If data is invalid
        """
        try:
            # Create smol-format file
            file_path = self.data_dir / f"{data_id}_{file_index:03d}.smol"

            # Encode and write data
            encoded_data = self.storage.encode(data)
            with open(file_path, 'wb') as f:
                f.write(encoded_data)

            # Save metadata
            metadata = self.storage.get_metadata(data)
            if additional_info:
                metadata.update(additional_info)
            self._save_metadata(data_id, file_index, metadata)

            logger.info(f"Successfully wrote data to {file_path}")
        except Exception as e:
            logger.error(f"Failed to write data: {e}")
            raise

    def read_data(
        self,
        data_id: str,
        file_index: int = 0
    ) -> Any:
        """
        Read data from smol-format files.

        Args:
            data_id: Data identifier
            file_index: Index for the file name

        Returns:
            Decoded data

        Raises:
            ValueError: If reading fails
        """
        try:
            file_path = self.data_dir / f"{data_id}_{file_index:03d}.smol"
            if not file_path.exists():
                return None

            with open(file_path, 'rb') as f:
                encoded_data = f.read()
            return self.storage.decode(encoded_data)
        except Exception as e:
            logger.error(f"Failed to read data: {e}")
            raise

    def get_metadata(self, data_id: str, file_index: int = 0) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a file.

        Args:
            data_id: Data identifier
            file_index: Index for the file name

        Returns:
            Metadata if available, None otherwise
        """
        return self._load_metadata(data_id, file_index)

    def list_files(self, data_id: Optional[str] = None) -> List[Tuple[str, int]]:
        """
        List available files.

        Args:
            data_id: Optional data identifier to filter by

        Returns:
            List of (data_id, file_index) tuples
        """
        try:
            pattern = f"{data_id}_*.smol" if data_id else "*.smol"
            files = []
            for path in self.data_dir.glob(pattern):
                parts = path.stem.split('_')
                if len(parts) == 2:
                    data_id, file_index = parts
                    files.append((data_id, int(file_index)))
            return sorted(files)
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            raise

    def delete_file(self, data_id: str, file_index: int) -> None:
        """
        Delete a file and its metadata.

        Args:
            data_id: Data identifier
            file_index: Index for the file name

        Raises:
            ValueError: If deletion fails
        """
        try:
            # Delete smol-format file
            file_path = self.data_dir / f"{data_id}_{file_index:03d}.smol"
            if file_path.exists():
                file_path.unlink()

            # Delete metadata
            metadata_path = self._get_metadata_path(data_id, file_index)
            if metadata_path.exists():
                metadata_path.unlink()

            logger.info(f"Successfully deleted {file_path}")
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            raise

    def backup(self, backup_dir: str) -> None:
        """
        Create a backup of all files.

        Args:
            backup_dir: Directory to store backup

        Raises:
            ValueError: If backup fails
        """
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)

            # Copy data directory
            shutil.copytree(self.data_dir, backup_path / "data", dirs_exist_ok=True)

            # Copy metadata directory
            if self.metadata_dir != self.data_dir:
                shutil.copytree(self.metadata_dir, backup_path / "metadata", dirs_exist_ok=True)

            logger.info(f"Successfully created backup in {backup_path}")
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise