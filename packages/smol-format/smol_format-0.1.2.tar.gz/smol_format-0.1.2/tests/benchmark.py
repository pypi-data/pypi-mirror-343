"""Performance benchmarks for smol-format."""
import time
import random
from pathlib import Path
import tempfile
import csv
from typing import List, Tuple
import statistics

from smol_format import SmolWriter, SmolReader, SmolStorage
from smol_format.core import (
    COMPRESSION_NONE,
    COMPRESSION_ZLIB,
    COMPRESSION_LZ4,
    COMPRESSION_ZSTD
)

def generate_points(num_points: int) -> List[Tuple[str, str]]:
    """Generate random points for testing."""
    points = []
    for _ in range(num_points):
        x = f"{random.randint(-1000000, 1000000)}/{random.randint(1, 1000)}"
        y = f"{random.randint(-1000000, 1000000)}/{random.randint(1, 1000)}"
        points.append((x, y))
    return points

def benchmark_write(
    points: List[Tuple[str, str]],
    compression_type: int,
    num_runs: int = 5
) -> float:
    """Benchmark writing points."""
    times = []
    for _ in range(num_runs):
        with tempfile.NamedTemporaryFile(suffix=".smol") as tmp:
            start = time.time()
            with SmolWriter(tmp.name, compression_type=compression_type) as writer:
                for x, y in points:
                    writer.add_point(x, y)
            end = time.time()
            times.append(end - start)
    return statistics.mean(times)

def benchmark_read(
    points: List[Tuple[str, str]],
    compression_type: int,
    use_mmap: bool,
    num_runs: int = 5
) -> float:
    """Benchmark reading points."""
    # Write points first
    with tempfile.NamedTemporaryFile(suffix=".smol") as tmp:
        with SmolWriter(tmp.name, compression_type=compression_type) as writer:
            for x, y in points:
                writer.add_point(x, y)

        # Read points
        times = []
        for _ in range(num_runs):
            start = time.time()
            with SmolReader(tmp.name) as reader:
                list(reader.read_points(use_mmap=use_mmap))
            end = time.time()
            times.append(end - start)
        return statistics.mean(times)

def benchmark_storage(
    points: List[Tuple[str, str]],
    num_runs: int = 5
) -> Tuple[float, float]:
    """Benchmark storage operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = SmolStorage(tmpdir)

        # Write
        write_times = []
        for _ in range(num_runs):
            start = time.time()
            storage.write_points("curve1", points)
            end = time.time()
            write_times.append(end - start)

        # Read
        read_times = []
        for _ in range(num_runs):
            start = time.time()
            list(storage.read_points("curve1"))
            end = time.time()
            read_times.append(end - start)

        return statistics.mean(write_times), statistics.mean(read_times)

def benchmark_migration(
    points: List[Tuple[str, str]],
    num_runs: int = 5
) -> float:
    """Benchmark CSV migration."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create CSV file
        csv_path = Path(tmpdir) / "test.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["x", "y"])
            for x, y in points:
                writer.writerow([x, y])

        # Migrate
        times = []
        for _ in range(num_runs):
            smol_path = Path(tmpdir) / f"test_{_}.smol"
            start = time.time()
            from smol_format.migrate import migrate_csv_to_smol
            migrate_csv_to_smol(csv_path, smol_path)
            end = time.time()
            times.append(end - start)
        return statistics.mean(times)

def run_benchmarks():
    """Run all benchmarks."""
    # Test sizes
    sizes = [1000, 10000, 100000]

    print("Running benchmarks...")
    print("\nWrite Performance (seconds):")
    print("Size\tNone\tZlib\tLZ4\tZstd")
    for size in sizes:
        points = generate_points(size)
        none_time = benchmark_write(points, COMPRESSION_NONE)
        zlib_time = benchmark_write(points, COMPRESSION_ZLIB)
        lz4_time = benchmark_write(points, COMPRESSION_LZ4)
        zstd_time = benchmark_write(points, COMPRESSION_ZSTD)
        print(f"{size}\t{none_time:.3f}\t{zlib_time:.3f}\t{lz4_time:.3f}\t{zstd_time:.3f}")

    print("\nRead Performance (seconds):")
    print("Size\tStandard\tMemory Mapped")
    for size in sizes:
        points = generate_points(size)
        std_time = benchmark_read(points, COMPRESSION_ZSTD, use_mmap=False)
        mmap_time = benchmark_read(points, COMPRESSION_ZSTD, use_mmap=True)
        print(f"{size}\t{std_time:.3f}\t{mmap_time:.3f}")

    print("\nStorage Performance (seconds):")
    print("Size\tWrite\tRead")
    for size in sizes:
        points = generate_points(size)
        write_time, read_time = benchmark_storage(points)
        print(f"{size}\t{write_time:.3f}\t{read_time:.3f}")

    print("\nMigration Performance (seconds):")
    print("Size\tTime")
    for size in sizes:
        points = generate_points(size)
        time = benchmark_migration(points)
        print(f"{size}\t{time:.3f}")

if __name__ == "__main__":
    run_benchmarks()