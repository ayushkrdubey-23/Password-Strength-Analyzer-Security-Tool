"""Tests for the educational Argon2id demonstration."""

import pytest

from argon2 import extract_parameters
from argon2.low_level import Type

from backend.services.argon2_demo import (
    hash_password_for_demo,
    verify_password_for_demo,
)


def test_hash_uses_argon2id():
    encoded_hash = hash_password_for_demo("Demo-Password-2026!")

    assert encoded_hash.startswith("$argon2id$")
    assert extract_parameters(encoded_hash).type == Type.ID


def test_hash_does_not_contain_plaintext_password():
    password = "Demo-Password-2026!"
    encoded_hash = hash_password_for_demo(password)

    assert password not in encoded_hash


def test_same_password_generates_different_hashes():
    password = "Demo-Password-2026!"

    first_hash = hash_password_for_demo(password)
    second_hash = hash_password_for_demo(password)

    assert first_hash != second_hash


def test_correct_password_verifies_successfully():
    password = "Demo-Password-2026!"
    encoded_hash = hash_password_for_demo(password)

    assert verify_password_for_demo(password, encoded_hash) is True


def test_incorrect_password_does_not_verify():
    encoded_hash = hash_password_for_demo("Correct-Password-2026!")

    assert verify_password_for_demo(
        "Incorrect-Password-2026!",
        encoded_hash
    ) is False


def test_empty_password_is_rejected_by_hash_function():
    with pytest.raises(ValueError):
        hash_password_for_demo("")


def test_non_string_password_is_rejected_by_hash_function():
    with pytest.raises(TypeError):
        hash_password_for_demo(123456)


def test_password_over_maximum_length_is_rejected():
    with pytest.raises(ValueError):
        hash_password_for_demo("A" * 1025)


def test_empty_password_is_rejected_by_verify_function():
    encoded_hash = hash_password_for_demo("Demo-Password-2026!")

    with pytest.raises(ValueError):
        verify_password_for_demo("", encoded_hash)


def test_non_string_password_is_rejected_by_verify_function():
    encoded_hash = hash_password_for_demo("Demo-Password-2026!")

    with pytest.raises(TypeError):
        verify_password_for_demo(123456, encoded_hash)


def test_non_string_hash_is_rejected():
    with pytest.raises(TypeError):
        verify_password_for_demo("Demo-Password-2026!", 123)


def test_empty_hash_is_rejected():
    with pytest.raises(ValueError):
        verify_password_for_demo("Demo-Password-2026!", "")


def test_malformed_hash_is_rejected():
    with pytest.raises(ValueError):
        verify_password_for_demo(
            "Demo-Password-2026!",
            "this-is-not-a-valid-argon2-hash"
        )


def test_oversized_hash_is_rejected():
    with pytest.raises(ValueError):
        verify_password_for_demo(
            "Demo-Password-2026!",
            "A" * 513
        )