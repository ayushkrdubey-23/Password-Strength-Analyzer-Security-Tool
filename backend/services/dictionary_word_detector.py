"""
Local Dictionary Word Detector.

Detects common dictionary words embedded inside passwords.

Privacy:
- Uses a local educational dataset.
- Makes no external API requests.
- Does not store or log submitted passwords.
- Does not return matched dictionary words.
"""

from functools import lru_cache
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_DICTIONARY_PATH = (
    PROJECT_ROOT / "data" / "common_words.txt"
)

MINIMUM_WORD_LENGTH = 4


@lru_cache(maxsize=8)
def _load_dictionary_words(dictionary_path):
    """
    Load dictionary words from a local text file.

    Returns:
        frozenset: Normalized dictionary words.

    Words shorter than the minimum supported length
    are ignored.
    """

    path = Path(dictionary_path)

    if not path.is_file():
        raise FileNotFoundError(
            "Dictionary-word dataset is unavailable."
        )

    words = set()

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            word = line.strip().casefold()

            if not word or word.startswith("#"):
                continue

            if len(word) < MINIMUM_WORD_LENGTH:
                continue

            if not word.isalpha():
                continue

            words.add(word)

    return frozenset(words)


def detect_dictionary_words(
    password: str,
    dictionary_path=None
) -> dict:
    """
    Detect dictionary words embedded inside a password.

    Matching is case-insensitive and supports words
    surrounded by numbers or special characters.

    The response contains only pattern types and lengths.
    It never contains the matched words or password.

    Args:
        password: Password to analyze.
        dictionary_path: Optional custom dataset path.

    Returns:
        dict: Detection status, pattern metadata,
        findings and suggestions.

    Raises:
        TypeError: If password is not a string.
        FileNotFoundError: If the dataset is unavailable.
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if dictionary_path is None:
        path = DEFAULT_DICTIONARY_PATH
    else:
        path = Path(dictionary_path)

    dictionary_words = _load_dictionary_words(
        str(path.resolve())
    )

    normalized_password = password.casefold()

    detected_patterns = []

    for word in dictionary_words:

        if word in normalized_password:

            detected_patterns.append({
                "type": "dictionary_word",
                "length": len(word)
            })

    # Sort by length for consistent results.
    detected_patterns.sort(
        key=lambda pattern: pattern["length"],
        reverse=True
    )

    findings = []

    suggestions = []

    if detected_patterns:

        findings.append(
            "One or more common dictionary words were detected "
            "inside the password."
        )

        suggestions.append(
            "Avoid using recognizable dictionary words, names "
            "or predictable word combinations. Consider a "
            "long, randomly generated password or passphrase."
        )

    return {
        "detected": bool(detected_patterns),
        "patterns": detected_patterns,
        "findings": findings,
        "suggestions": suggestions
    }