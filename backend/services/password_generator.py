
"""
Secure Password Generator.

Uses Python's secrets module for cryptographically
secure random character selection and shuffling.

Generated passwords are returned only to the caller.
This module does not store or log generated passwords.
"""

import secrets
import string


LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"


def generate_password(
    length: int = 20,
    include_lowercase: bool = True,
    include_uppercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True
) -> str:
    """
    Generate a cryptographically secure random password.

    Args:
        length: Password length, from 8 to 128.
        include_lowercase: Include lowercase letters.
        include_uppercase: Include uppercase letters.
        include_digits: Include numeric digits.
        include_symbols: Include special characters.

    Returns:
        A securely generated password string.

    Raises:
        TypeError: If length is not an integer or category
                   selections are not boolean.
        ValueError: If length is outside the allowed range
                    or no character category is selected.
    """

    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError("Password length must be an integer.")

    if not 8 <= length <= 128:
        raise ValueError(
            "Password length must be between 8 and 128."
        )

    category_options = {
        "lowercase": (include_lowercase, LOWERCASE),
        "uppercase": (include_uppercase, UPPERCASE),
        "digits": (include_digits, DIGITS),
        "symbols": (include_symbols, SYMBOLS)
    }

    for name, (enabled, _) in category_options.items():
        if not isinstance(enabled, bool):
            raise TypeError(
                f"{name} selection must be a boolean."
            )

    selected_categories = [
        characters
        for enabled, characters in category_options.values()
        if enabled
    ]

    if not selected_categories:
        raise ValueError(
            "Select at least one character category."
        )

    if length < len(selected_categories):
        raise ValueError(
            "Password length is too short for the selected categories."
        )

    # Guarantee at least one character from each selected category.
    password_characters = [
        secrets.choice(characters)
        for characters in selected_categories
    ]

    # Combine all enabled character categories.
    combined_characters = "".join(selected_categories)

    # Fill the remaining password positions securely.
    remaining_length = length - len(password_characters)

    password_characters.extend(
        secrets.choice(combined_characters)
        for _ in range(remaining_length)
    )

    # Securely shuffle the characters to avoid predictable positions.
    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)
