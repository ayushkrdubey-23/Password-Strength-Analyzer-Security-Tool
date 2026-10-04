
"""
Password Character Analyzer

Detects character categories and calculates
character diversity metrics.

Supported categories:
- Lowercase
- Uppercase
- Digits
- Symbols
- Spaces
"""


def analyze_characters(password):
    """
    Analyze password character composition.

    Args:
        password (str): Password submitted for analysis.

    Returns:
        dict: Character metrics and category information.

    Notes:
        Unicode-aware Python character methods are used.
        Whitespace is treated separately from symbols.
        No password value is returned or stored.
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    length = len(password)

    has_lowercase = any(
        char.islower() for char in password
    )

    has_uppercase = any(
        char.isupper() for char in password
    )

    has_digits = any(
        char.isdigit() for char in password
    )

    has_symbols = any(
        not char.isalnum() and not char.isspace()
        for char in password
    )

    has_spaces = any(
        char.isspace() for char in password
    )

    unique_character_count = len(set(password))

    unique_character_ratio = (
        unique_character_count / length
        if length > 0
        else 0.0
    )

    character_types = {
        "lowercase": has_lowercase,
        "uppercase": has_uppercase,
        "digits": has_digits,
        "symbols": has_symbols,
        "spaces": has_spaces
    }

    character_type_count = sum(
        character_types.values()
    )

    return {
        "length": length,

        "character_types": character_types,

        "unique_character_count": unique_character_count,

        "character_type_count": character_type_count,

        "unique_character_ratio": round(
            unique_character_ratio,
            4
        )
    }
