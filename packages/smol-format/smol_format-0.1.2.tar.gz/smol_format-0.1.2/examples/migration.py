"""Migration examples for smol-format."""
import csv
from pathlib import Path
import tempfile
from typing import List, Tuple

from smol_format import migrate_directory, migrate_csv_to_smol
from smol_format.migrate import validate_csv_file, backup_csv_files, restore_from_backup

def create_sample_csv(path: Path, num_points: int) -> None:
    """Create a sample CSV file."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y"])
        for i in range(num_points):
            writer.writerow([f"{i}/1", f"{i*2}/1"])

def basic_migration():
    """Basic migration example."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create sample CSV
        csv_path = tmpdir / "points.csv"
        create_sample_csv(csv_path, 1000)

        # Migrate to smol
        smol_path = tmpdir / "points.smol"
        migrate_csv_to_smol(
            csv_path,
            smol_path,
            additional_info={"description": "Migrated points"}
        )

        print(f"Migrated {csv_path} to {smol_path}")

def directory_migration():
    """Directory migration example."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create sample CSV files
        csv_dir = tmpdir / "csv"
        csv_dir.mkdir()

        for i in range(3):
            csv_path = csv_dir / f"points_{i}.csv"
            create_sample_csv(csv_path, 1000)

        # Migrate directory
        smol_dir = tmpdir / "smol"
        migrate_directory(
            csv_dir,
            smol_dir,
            show_progress=True,
            additional_info={"description": "Migrated directory"}
        )

        print(f"Migrated {csv_dir} to {smol_dir}")

def backup_and_restore():
    """Backup and restore example."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create sample CSV files
        csv_dir = tmpdir / "csv"
        csv_dir.mkdir()

        for i in range(3):
            csv_path = csv_dir / f"points_{i}.csv"
            create_sample_csv(csv_path, 1000)

        # Create backup
        backup_dir = tmpdir / "backup"
        backup_csv_files(csv_dir, backup_dir)
        print(f"Created backup in {backup_dir}")

        # Restore from backup
        restore_dir = tmpdir / "restore"
        restore_from_backup(backup_dir, restore_dir)
        print(f"Restored from backup to {restore_dir}")

def validation_example():
    """CSV validation example."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create valid CSV
        valid_csv = tmpdir / "valid.csv"
        create_sample_csv(valid_csv, 1000)
        print(f"Valid CSV: {validate_csv_file(valid_csv)}")

        # Create invalid CSV
        invalid_csv = tmpdir / "invalid.csv"
        with open(invalid_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["x"])  # Missing y column
            writer.writerow(["123/456"])
        print(f"Invalid CSV: {validate_csv_file(invalid_csv)}")

if __name__ == "__main__":
    print("Running basic migration example...")
    basic_migration()

    print("\nRunning directory migration example...")
    directory_migration()

    print("\nRunning backup and restore example...")
    backup_and_restore()

    print("\nRunning validation example...")
    validation_example()