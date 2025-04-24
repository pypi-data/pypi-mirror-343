"""
Example of using custom optimizers with smol-format.
"""
import numpy as np
import pandas as pd
from datetime import datetime
from smol_format import DenseStorage, StorageConfig, TypeOptimizer
import pyarrow as pa
import pyarrow.compute as pc

def main():
    # Create custom optimizer for rational numbers
    rational_optimizer = TypeOptimizer(
        name="rational_optimize",
        type=str,
        optimize_func=lambda arr: pc.dictionary_encode(arr),
        validate_func=lambda x: isinstance(x, str) and '/' in x
    )

    # Create storage with custom optimizer
    storage = DenseStorage(
        config=StorageConfig(
            compression_level=3,
            optimize_types=True,
            custom_optimizers=[rational_optimizer]
        )
    )

    # Create sample data with rational numbers
    data = {
        'x': ['123/456', '789/101', '202/303'],
        'y': ['404/505', '606/707', '808/909'],
        'height': [10.0, 20.0, 30.0],
        'timestamp': [datetime.now(), datetime.now(), datetime.now()]
    }
    df = pd.DataFrame(data)

    # Get optimization stats
    stats = storage.get_optimization_stats(df)
    print("Optimization Statistics:")
    print(f"Original size: {stats['original_size']} bytes")
    print(f"Optimized size: {stats['optimized_size']} bytes")
    print(f"Compression ratio: {stats['compression_ratio']:.2f}x")
    print("\nColumn Statistics:")
    for col, col_stats in stats['column_stats'].items():
        print(f"{col}:")
        print(f"  Type: {col_stats['type']}")
        print(f"  Optimized: {col_stats['optimized']}")

    # Encode and decode data
    encoded = storage.encode(df)
    decoded = storage.decode(encoded)

    print("\nDecoded Data:")
    print(decoded)

if __name__ == '__main__':
    main()