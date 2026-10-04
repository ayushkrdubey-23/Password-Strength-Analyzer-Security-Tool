
"""
Local Common Password Checker.

This module checks submitted passwords against
a small local educational dataset.

Privacy:
- No external API requests.
- No password logging.
- No password persistence.
- No submitted passwords added to the dataset.
"""

from functools import lru_cache
from pathlib import Path


# Resolve the project root from this file's location.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_DATASET_PATH = (
    PROJECT_ROOT / "data" / "common_passwords.txt"
)


@lru_cache(maxsize=8)
def _load_common_passwords(dataset_path):
    """
    Load common passwords into memory.

    Args:
        dataset_path (str): Absolute or relative dataset path.

    Returns:
        frozenset: Normalized common-password entries.

    The dataset is cached to avoid repeated file reads.
    """

    path = Path(dataset_path)

    if not path.is_file():
        raise FileNotFoundError(
            "Common-password dataset is unavailable."
        )

    common_passwords = set()

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            entry = line.strip()

            # Ignore blank lines and comments.
            if not entry or entry.startswith("#"):
                continue

            common_passwords.add(entry.casefold())

    return frozenset(common_passwords)


def is_common_password(password, dataset_path=None):
    """
    Check whether a password exactly matches a
    locally maintained common-password entry.

    Args:
        password (str): Submitted password.
        dataset_path (str | Path | None): Optional
            custom dataset path for testing.

    Returns:
        bool: True if a match exists, otherwise False.

    Important:
        The submitted password is not stripped because
        whitespace can be a meaningful password character.
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if dataset_path is None:
        path = DEFAULT_DATASET_PATH
    else:
        path = Path(dataset_path)

    common_passwords = _load_common_passwords(
        str(path.resolve())
    )

    return password.casefold() in common_passwords
