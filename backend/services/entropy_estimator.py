"""
Educational Password Entropy Estimator.

Estimates theoretical entropy using the observed ASCII
character categories.

Formula:
    entropy = password_length * log2(character_pool_size)

This is an educational approximation, not a guarantee
of real-world password unpredictability.

Privacy:
- Does not store or log passwords.
- Does not return password characters.
- Does not make external requests.
"""

import math
import string


CHARACTER_POOL_SIZES = {
    "lowercase": 26,
    "uppercase": 26,
    "digits": 10,
    "symbols": 32,
    "spaces": 1,
}


def estimate_entropy(password: str) -> dict:
    """
    Estimate theoretical password entropy.

    Only printable ASCII characters are supported by this
    simple character-pool model. Unsupported characters
    produce an unavailable estimate rather than a misleading
    numerical result.

    Args:
        password: Password submitted for analysis.

    Returns:
        Dictionary containing the entropy estimate and limitations.

    Raises:
        TypeError: If password is not a string.
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        return {
            "estimate_available": True,
            "estimated_bits": 0.0,
            "character_pool_size": 0,
            "length": 0,
            "interpretation": "NO PASSWORD",
            "assumption": (
                "The estimate assumes independent, uniformly "
                "selected characters."
            ),
            "limitations": [
                "An empty password provides no meaningful protection.",
                "This is not a measurement of actual password security.",
            ],
            "findings": [
                "No password characters are available for entropy estimation."
            ],
            "suggestions": [
                "Use a long, unique password or randomly generated passphrase."
            ],
        }

    supported_characters = (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
        + string.punctuation
        + " "
    )

    unsupported_characters_present = any(
        character not in supported_characters
        for character in password
    )

    if unsupported_characters_present:
        return {
            "estimate_available": False,
            "estimated_bits": None,
            "character_pool_size": None,
            "length": len(password),
            "interpretation": "NOT ESTIMATED",
            "assumption": (
                "The current educational model supports printable ASCII "
                "characters only."
            ),
            "limitations": [
                "One or more characters are outside the supported printable ASCII set.",
                "Unicode and non-standard whitespace character pools are not modeled.",
                "This is not a measurement of actual password security.",
            ],
            "findings": [
                "Entropy estimation is unavailable for this character set."
            ],
            "suggestions": [
                "Use the other password analysis results as additional guidance. "
                "Do not interpret an unavailable estimate as a weak password."
            ],
        }

    categories_present = {
        "lowercase": any(
            character in string.ascii_lowercase
            for character in password
        ),
        "uppercase": any(
            character in string.ascii_uppercase
            for character in password
        ),
        "digits": any(
            character in string.digits
            for character in password
        ),
        "symbols": any(
            character in string.punctuation
            for character in password
        ),
        "spaces": " " in password,
    }

    character_pool_size = sum(
        CHARACTER_POOL_SIZES[category]
        for category, present in categories_present.items()
        if present
    )

    estimated_bits = (
        len(password) * math.log2(character_pool_size)
        if character_pool_size > 0
        else 0.0
    )

    estimated_bits = round(estimated_bits, 2)

    if estimated_bits < 28:
        interpretation = "VERY LOW THEORETICAL ENTROPY"
    elif estimated_bits < 36:
        interpretation = "LOW THEORETICAL ENTROPY"
    elif estimated_bits < 60:
        interpretation = "MODERATE THEORETICAL ENTROPY"
    elif estimated_bits < 80:
        interpretation = "HIGH THEORETICAL ENTROPY"
    else:
        interpretation = "VERY HIGH THEORETICAL ENTROPY"

    limitations = [
        "Assumes every character is independently and uniformly selected.",
        "Does not account for dictionary words, dates, keyboard walks, or repeated patterns.",
        "Human password choices are often more predictable than this model assumes.",
        "The result is educational and is not a cryptographic security guarantee.",
    ]

    return {
        "estimate_available": True,
        "estimated_bits": estimated_bits,
        "character_pool_size": character_pool_size,
        "length": len(password),
        "interpretation": interpretation,
        "assumption": (
            "Each character is assumed to be independently and uniformly "
            "selected from the estimated character pool."
        ),
        "limitations": limitations,
        "findings": [
            "Theoretical entropy was estimated using password length "
            "and observed ASCII character categories."
        ],
        "suggestions": [
            "Prefer long, unique, randomly generated passwords or passphrases.",
            "Avoid predictable words, dates, sequences, and repeated patterns.",
        ],
    }
