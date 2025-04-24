"""
Migration utilities for smol-format files.
"""
import csv
from pathlib import Path
from typing import List, Tuple, Optional, Callable, Dict, Any
import logging
from datetime import datetime
import shutil
from tqdm import tqdm

from smol_format.core import SmolWriter, COMPRESSION_ZSTD, SmolError, ValidationError
from smol_format.storage import SmolStorage, SmolMetadata

logger = logging.getLogger(__name__)

def migrate_csv_to_smol(
    csv_path: Path,
    smol_path: Path,
    compress: bool = True,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    additional_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Migrate points from CSV to smol-format.

    Args:
        csv_path: Path to CSV file
        smol_path: Path to write smol-format file
        compress: Whether to compress the smol-format file
        progress_callback: Optional callback for progress updates
        additional_info: Additional metadata to store

    Raises:
        ValidationError: If CSV data is invalid
        SmolError: If migration fails
    """
    logger.info(f"Migrating {csv_path} to {smol_path}")

    try:
        # Read CSV
        points: List[Tuple[str, str]] = []
        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) < 2:
                    raise ValidationError(f"Invalid CSV row: {row}")
                x, y = row[0], row[1]
                points.append((x, y))

        # Write smol
        writer = SmolWriter(
            smol_path,
            compression_type=COMPRESSION_ZSTD if compress else 0
        )

        # Add points with progress tracking
        total_points = len(points)
        for i, (x, y) in enumerate(points, 1):
            writer.add_point(x, y)
            if progress_callback:
                progress_callback(i, total_points)

        writer.write()

        # Save metadata
        metadata = SmolMetadata(
            curve_id=smol_path.stem,
            file_index=0,
            created_at=datetime.now(),
            num_points=total_points,
            coord_bits=writer.coord_bits,
            compression_type=writer.compression_type,
            additional_info=additional_info
        )

        # Create storage instance for metadata
        storage = SmolStorage(smol_path.parent)
        storage._save_metadata(metadata)

        logger.info(f"Migration complete: {smol_path}")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise SmolError(f"Migration failed: {e}")

def migrate_directory(
    csv_dir: Path,
    smol_dir: Path,
    compress: bool = True,
    show_progress: bool = True,
    additional_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Migrate all CSV files in a directory.

    Args:
        csv_dir: Directory containing CSV files
        smol_dir: Directory to write smol-format files
        compress: Whether to compress smol-format files
        show_progress: Whether to show progress bar
        additional_info: Additional metadata to store

    Raises:
        SmolError: If migration fails
    """
    logger.info(f"Migrating directory: {csv_dir}")

    try:
        # Create output directory
        smol_dir.mkdir(parents=True, exist_ok=True)

        # Get list of CSV files
        csv_files = list(csv_dir.glob("*.csv"))
        if not csv_files:
            logger.warning(f"No CSV files found in {csv_dir}")
            return

        # Process each CSV file
        if show_progress:
            pbar = tqdm(csv_files, desc="Migrating files")
        else:
            pbar = csv_files

        for csv_path in pbar:
            smol_path = smol_dir / f"{csv_path.stem}.smol"

            def progress_callback(current: int, total: int) -> None:
                if show_progress:
                    pbar.set_postfix({"points": f"{current}/{total}"})

            migrate_csv_to_smol(
                csv_path,
                smol_path,
                compress=compress,
                progress_callback=progress_callback,
                additional_info=additional_info
            )

        logger.info("Directory migration complete")
    except Exception as e:
        logger.error(f"Directory migration failed: {e}")
        raise SmolError(f"Directory migration failed: {e}")

def validate_csv_file(csv_path: Path) -> bool:
    """
    Validate a CSV file.

    Args:
        csv_path: Path to CSV file

    Returns:
        True if valid, False otherwise
    """
    try:
        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            if len(header) < 2:
                return False

            for row in reader:
                if len(row) < 2:
                    return False
                try:
                    x, y = row[0], row[1]
                    # Try to convert to integers
                    int(x.split('/')[0])
                    int(y.split('/')[0])
                except (ValueError, IndexError):
                    return False

        return True
    except Exception:
        return False

def backup_csv_files(csv_dir: Path, backup_dir: Path) -> None:
    """
    Create a backup of CSV files.

    Args:
        csv_dir: Directory containing CSV files
        backup_dir: Directory to store backup

    Raises:
        SmolError: If backup fails
    """
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(csv_dir, backup_dir / "csv", dirs_exist_ok=True)
        logger.info(f"Successfully backed up CSV files to {backup_dir}")
    except Exception as e:
        logger.error(f"Failed to backup CSV files: {e}")
        raise SmolError(f"Failed to backup CSV files: {e}")

def restore_from_backup(backup_dir: Path, target_dir: Path) -> None:
    """
    Restore files from backup.

    Args:
        backup_dir: Directory containing backup
        target_dir: Directory to restore to

    Raises:
        SmolError: If restoration fails
    """
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(backup_dir, target_dir, dirs_exist_ok=True)
        logger.info(f"Successfully restored files from {backup_dir}")
    except Exception as e:
        logger.error(f"Failed to restore from backup: {e}")
        raise SmolError(f"Failed to restore from backup: {e}")