"""
Example demonstrating how to store scientific data with exact rational numbers using smol-format.
"""
from smol_format import DenseStorage, StorageConfig
from typing import Dict, List, Union
import math

def generate_fibonacci_ratios(n: int) -> List[str]:
    """Generate ratios of consecutive Fibonacci numbers."""
    def fib(n: int) -> int:
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b

    ratios = []
    for i in range(2, n + 2):
        fn = fib(i)
        fn_minus_1 = fib(i - 1)
        ratio = f"{fn}/{fn_minus_1}"
        ratios.append(ratio)

    return ratios

def generate_continued_fraction_convergents(x: float, n: int) -> List[str]:
    """Generate continued fraction convergents for a real number."""
    def continued_fraction_terms(x: float, n: int) -> List[int]:
        terms = []
        for _ in range(n):
            a = math.floor(x)
            terms.append(a)
            if x == a:
                break
            x = 1 / (x - a)
        return terms

    def evaluate_convergent(terms: List[int]) -> str:
        num, den = 1, 0
        prev_num, prev_den = 0, 1

        for term in reversed(terms):
            num, prev_num = term * num + prev_num, num
            den, prev_den = term * den + prev_den, den

        return f"{num}/{den}"

    terms = continued_fraction_terms(x, n)
    convergents = []

    for i in range(1, len(terms) + 1):
        convergent = evaluate_convergent(terms[:i])
        convergents.append(convergent)

    return convergents

def main():
    # Initialize storage
    storage = DenseStorage(
        config=StorageConfig(
            compression_level=3,
            encoding="json"
        )
    )

    # Generate scientific data
    data: Dict[str, Dict[str, Union[List[str], str]]] = {
        "fibonacci": {
            "description": "Ratios of consecutive Fibonacci numbers (converging to φ)",
            "ratios": generate_fibonacci_ratios(20)
        },
        "pi_convergents": {
            "description": "Continued fraction convergents for π",
            "convergents": generate_continued_fraction_convergents(math.pi, 10)
        },
        "e_convergents": {
            "description": "Continued fraction convergents for e",
            "convergents": generate_continued_fraction_convergents(math.e, 10)
        }
    }

    print("Original Data:")
    print("-------------")
    for category, values in data.items():
        print(f"\n{category}:")
        print(f"Description: {values['description']}")
        print("Values:")
        for i, value in enumerate(next(v for v in values.values() if isinstance(v, list))):
            print(f"  {i+1}: {value}")

    # Encode the data
    encoded = storage.encode(data)
    print(f"\nEncoded size: {len(encoded)} bytes")

    # Decode the data
    decoded = storage.decode(encoded)

    # Verify data preservation
    print("\nVerifying data preservation:")
    print("---------------------------")
    for category in data:
        original_values = next(v for v in data[category].values() if isinstance(v, list))
        decoded_values = next(v for v in decoded[category].values() if isinstance(v, list))
        preserved = original_values == decoded_values
        print(f"{category}: {'✓' if preserved else '✗'} (preserved exactly)")

    # Get metadata
    metadata = storage.get_metadata(data)
    print("\nMetadata:")
    print("---------")
    for key, value in metadata.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()