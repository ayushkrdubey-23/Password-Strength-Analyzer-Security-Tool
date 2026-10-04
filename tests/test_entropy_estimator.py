"""Tests for the educational password entropy estimator."""

import math

import pytest

from backend.services.entropy_estimator import (
    estimate_entropy,
)


def test_lowercase_only_password_uses_26_character_pool():
    result = estimate_entropy("abcdef")

    assert result["character_pool_size"] == 26
    assert result["estimate_available"] is True


def test_uppercase_only_password_uses_26_character_pool():
    result = estimate_entropy("ABCDEF")

    assert result["character_pool_size"] == 26


def test_digits_only_password_uses_10_character_pool():
    result = estimate_entropy("123456")

    assert result["character_pool_size"] == 10


def test_symbols_only_password_uses_32_character_pool():
    result = estimate_entropy("!@#$%^")

    assert result["character_pool_size"] == 32


def test_space_adds_one_to_character_pool():
    result = estimate_entropy("hello world")

    assert result["character_pool_size"] == 27


def test_all_ascii_categories_use_94_character_pool():
    result = estimate_entropy("Abc123!@")

    assert result["character_pool_size"] == 94


def test_entropy_formula_is_applied_correctly():
    password = "Abc123!@"

    result = estimate_entropy(password)

    expected = round(
        len(password) * math.log2(94),
        2,
    )

    assert result["estimated_bits"] == expected


def test_longer_password_has_higher_theoretical_entropy():
    short_result = estimate_entropy("Abc123!")
    long_result = estimate_entropy("Abc123!Def456@")

    assert (
        long_result["estimated_bits"]
        > short_result["estimated_bits"]
    )


def test_empty_password_returns_zero_entropy():
    result = estimate_entropy("")

    assert result["estimate_available"] is True
    assert result["estimated_bits"] == 0.0
    assert result["character_pool_size"] == 0
    assert result["interpretation"] == "NO PASSWORD"


def test_unicode_password_returns_unavailable_estimate():
    result = estimate_entropy("Café123!")

    assert result["estimate_available"] is False
    assert result["estimated_bits"] is None
    assert result["character_pool_size"] is None
    assert result["interpretation"] == "NOT ESTIMATED"


def test_non_standard_whitespace_returns_unavailable_estimate():
    result = estimate_entropy("Abc123!\t")

    assert result["estimate_available"] is False


def test_result_does_not_return_password():
    password = "Synthetic!Password987"

    result = estimate_entropy(password)

    assert password not in str(result)


def test_result_explains_entropy_assumptions():
    result = estimate_entropy("Abc123!@")

    assert "independently" in result["assumption"]
    assert len(result["limitations"]) >= 3


def test_result_contains_findings_and_suggestions():
    result = estimate_entropy("Abc123!@")

    assert isinstance(result["findings"], list)
    assert isinstance(result["suggestions"], list)


def test_non_string_input_raises_type_error():
    with pytest.raises(TypeError):
        estimate_entropy(123456)