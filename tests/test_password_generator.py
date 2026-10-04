
import string

import pytest

from backend.services.password_generator import (
    generate_password,
    LOWERCASE,
    UPPERCASE,
    DIGITS,
    SYMBOLS
)


def test_default_generator_returns_twenty_characters():
    password = generate_password()

    assert len(password) == 20


def test_custom_password_length():
    password = generate_password(length=32)

    assert len(password) == 32


def test_minimum_password_length():
    password = generate_password(length=8)

    assert len(password) == 8


def test_maximum_password_length():
    password = generate_password(length=128)

    assert len(password) == 128


def test_default_password_contains_all_categories():
    password = generate_password()

    assert any(char in LOWERCASE for char in password)
    assert any(char in UPPERCASE for char in password)
    assert any(char in DIGITS for char in password)
    assert any(char in SYMBOLS for char in password)


def test_lowercase_only_generation():
    password = generate_password(
        length=12,
        include_lowercase=True,
        include_uppercase=False,
        include_digits=False,
        include_symbols=False
    )

    assert len(password) == 12
    assert all(char in LOWERCASE for char in password)


def test_uppercase_only_generation():
    password = generate_password(
        length=12,
        include_lowercase=False,
        include_uppercase=True,
        include_digits=False,
        include_symbols=False
    )

    assert all(char in UPPERCASE for char in password)


def test_digits_only_generation():
    password = generate_password(
        length=12,
        include_lowercase=False,
        include_uppercase=False,
        include_digits=True,
        include_symbols=False
    )

    assert all(char in DIGITS for char in password)


def test_symbols_only_generation():
    password = generate_password(
        length=12,
        include_lowercase=False,
        include_uppercase=False,
        include_digits=False,
        include_symbols=True
    )

    assert all(char in SYMBOLS for char in password)


def test_selected_categories_are_included():
    password = generate_password(
        length=16,
        include_lowercase=True,
        include_uppercase=False,
        include_digits=True,
        include_symbols=False
    )

    assert any(char in LOWERCASE for char in password)
    assert any(char in DIGITS for char in password)
    assert all(
        char in LOWERCASE + DIGITS
        for char in password
    )


def test_every_generated_password_has_requested_length():
    for length in (8, 12, 16, 24, 32, 64, 128):
        password = generate_password(length=length)

        assert len(password) == length


def test_repeated_calls_generate_passwords():
    passwords = {
        generate_password(length=24)
        for _ in range(10)
    }

    # This is a basic randomness sanity check, not a
    # mathematical proof of uniqueness or security.
    assert len(passwords) > 1


@pytest.mark.parametrize("invalid_length", [0, 1, 7, 129, -10])
def test_rejects_length_outside_allowed_range(invalid_length):
    with pytest.raises(ValueError):
        generate_password(length=invalid_length)


@pytest.mark.parametrize("invalid_length", ["16", 12.5, None, True])
def test_rejects_non_integer_length(invalid_length):
    with pytest.raises(TypeError):
        generate_password(length=invalid_length)


def test_rejects_when_no_category_is_selected():
    with pytest.raises(ValueError):
        generate_password(
            include_lowercase=False,
            include_uppercase=False,
            include_digits=False,
            include_symbols=False
        )


def test_rejects_non_boolean_category_selection():
    with pytest.raises(TypeError):
        generate_password(include_digits=1)


def test_generated_password_contains_only_allowed_characters():
    password = generate_password(length=40)

    allowed_characters = (
        string.ascii_letters
        + string.digits
        + SYMBOLS
    )

    assert all(char in allowed_characters for char in password)


def test_generator_returns_a_string():
    password = generate_password()

    assert isinstance(password, str)
    