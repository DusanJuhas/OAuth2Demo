"""
keyGenerator.py
----------------
Generates a secure 32‑byte random secret key and stores it
in a binary file named 'my_secret.key'.

This key can be used for signing sessions or other cryptographic
needs in the demo application.

Usage:
    python keyGenerator.py
"""

import secrets

KEYFILE = "my_secret.key"

def generate_secret_key(filename: str = KEYFILE, num_bytes: int = 32):
    """
    Generates a secure random binary key and writes it to a file.

    Args:
        filename (str): Output file name. Defaults to 'my_secret.key'.
        num_bytes (int): Number of random bytes to generate. Defaults to 32.
    """
    key = secrets.token_bytes(num_bytes)

    with open(filename, "wb") as f:
        f.write(key)

    print(f"Successfully generated {num_bytes}-byte secret key in '{filename}'.")


if __name__ == "__main__":
    generate_secret_key()
