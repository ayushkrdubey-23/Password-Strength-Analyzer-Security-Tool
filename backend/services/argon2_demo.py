"""Educational Argon2id password hashing demonstration.

This module does not store passwords or hashes. It only demonstrates
hash generation and verification in memory.
"""

from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)
from argon2.low_level import Type


# Explicit educational configuration.
# Production applications should review parameters against their
# deployment environment and current security guidance.
_password_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=19456,
    parallelism=1,
    hash_len=32,
    salt_len=16,
    type=Type.ID,
)


def hash_password_for_demo(password):
    """Generate an Argon2id hash without saving the password or hash."""

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        raise ValueError("Password cannot be empty.")

    if len(password) > 1024:
        raise ValueError("Password exceeds the maximum allowed length.")

    return _password_hasher.hash(password)


def verify_password_for_demo(password, encoded_hash):
    """Verify a password against an Argon2 encoded hash."""

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        raise ValueError("Password cannot be empty.")

    if len(password) > 1024:
        raise ValueError("Password exceeds the maximum allowed length.")

    if not isinstance(encoded_hash, str):
        raise TypeError("Encoded hash must be a string.")

    if not encoded_hash:
        raise ValueError("Encoded hash cannot be empty.")

    if len(encoded_hash) > 512:
        raise ValueError("Encoded hash is invalid.")

    try:
        return _password_hasher.verify(encoded_hash, password)

    except VerifyMismatchError:
        return False

    except (InvalidHashError, VerificationError):
        raise ValueError("The supplied encoded hash is invalid.") from None