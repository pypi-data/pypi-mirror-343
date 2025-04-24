"""
Example demonstrating how to store and retrieve large rational numbers using smol-format.
"""
from smol_format import DenseStorage, StorageConfig

def main():
    # Initialize storage
    storage = DenseStorage(
        config=StorageConfig(
            compression_level=3,
            encoding="json"
        )
    )

    # Example data with large rational numbers
    # These are approximations of π and e with high precision
    data = {
        "constants": {
            "pi": "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679/10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
            "e": "271828182845904523536028747135266249775724709369995957496696762772407663035354759457138217852516642/100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        },
        "calculations": {
            "large_fraction": "123456789012345678901234567890123456789012345678901234567890/987654321098765432109876543210987654321098765432109876543210",
            "simple_fraction": "355/113"  # A good approximation of π
        }
    }

    print("Original Data:")
    print("-------------")
    for category, values in data.items():
        print(f"\n{category}:")
        for name, value in values.items():
            print(f"{name}: {value}")

    # Encode the data
    encoded = storage.encode(data)
    print(f"\nEncoded size: {len(encoded)} bytes")

    # Decode the data
    decoded = storage.decode(encoded)

    print("\nVerifying data preservation:")
    print("---------------------------")
    for category, values in decoded.items():
        print(f"\n{category}:")
        for name, value in values.items():
            original = data[category][name]
            preserved = value == original
            print(f"{name}: {'✓' if preserved else '✗'} (preserved exactly)")

    # Get metadata
    metadata = storage.get_metadata(data)
    print("\nMetadata:")
    print("---------")
    for key, value in metadata.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()