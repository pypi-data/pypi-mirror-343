"""
Example demonstrating how to stream large datasets using smol-format.
"""
from smol_format import DenseStorage, StorageConfig
from typing import Iterator, Dict, List
import random

def generate_large_rationals(n: int) -> Iterator[Dict[str, List[str]]]:
    """Generate chunks of large rational numbers."""
    chunk_size = 1000
    current_chunk = []

    for i in range(n):
        # Generate a large rational number
        numerator = random.randint(10**50, 10**100)
        denominator = random.randint(10**50, 10**100)
        rational = f"{numerator}/{denominator}"

        current_chunk.append(rational)

        if len(current_chunk) >= chunk_size:
            yield {"rationals": current_chunk}
            current_chunk = []

    if current_chunk:
        yield {"rationals": current_chunk}

def main():
    # Initialize storage
    storage = DenseStorage(
        config=StorageConfig(
            compression_level=3,
            encoding="json"
        )
    )

    # Generate a stream of large rational numbers
    total_numbers = 10000
    print(f"Generating {total_numbers} large rational numbers...")

    # Stream encode the data
    encoded_chunks = []
    total_encoded_size = 0

    print("\nEncoding stream:")
    print("---------------")
    for i, chunk in enumerate(generate_large_rationals(total_numbers)):
        encoded = storage.encode(chunk)
        encoded_chunks.append(encoded)
        total_encoded_size += len(encoded)
        print(f"Chunk {i+1}: {len(encoded)} bytes")

    print(f"\nTotal encoded size: {total_encoded_size} bytes")

    # Stream decode the data
    print("\nDecoding stream:")
    print("---------------")
    total_rationals = 0

    for i, chunk in enumerate(encoded_chunks):
        decoded = storage.decode(chunk)
        chunk_size = len(decoded["rationals"])
        total_rationals += chunk_size

        # Print the first rational number in each chunk
        first_rational = decoded["rationals"][0]
        print(f"Chunk {i+1} ({chunk_size} numbers): {first_rational[:50]}.../{first_rational[-50:]})")

    print(f"\nTotal numbers processed: {total_rationals}")

if __name__ == "__main__":
    main()