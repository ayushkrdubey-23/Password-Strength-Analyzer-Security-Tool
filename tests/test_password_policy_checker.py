"""Tests for the password policy checker."""

import pytest

from backend.services.password_policy_checker import (
    check_password_policy,
)


def test_policy_returns_all_ten_checks():
    result = check_password_policy("Violet!Cedar#74Moon")

    assert result["total_checks"] == 10
    assert len(result["checks"]) == 10


def test_policy_contains_expected_check_ids():
    result = check_password_policy("Violet!Cedar#74Moon")

    check_ids = {
        check["id"]
        for check in result["checks"]
    }

    assert check_ids == {
        "minimum_length",
        "lowercase",
        "uppercase",
        "digits",
        "symbols",
        "not_common",
        "no_sequences",
        "no_keyboard_patterns",
        "no_repetitions",
        "no_predictable_patterns",
    }


def test_strong_example_passes_default_policy():
    result = check_password_policy("Violet!Cedar#74Moon")

    assert result["compliant"] is True
    assert result["failed_checks"] == 0
    assert result["passed_checks"] == 10
    assert result["recommendations"] == []


def test_short_password_fails_minimum_length():
    result = check_password_policy("Ab1!")

    length_check = next(
        check for check in result["checks"]
        if check["id"] == "minimum_length"
    )

    assert length_check["passed"] is False


def test_password_without_lowercase_fails():
    result = check_password_policy("ABCDEFGHIJKL1!")

    check = next(
        item for item in result["checks"]
        if item["id"] == "lowercase"
    )

    assert check["passed"] is False


def test_password_without_uppercase_fails():
    result = check_password_policy("abcdefghijkl1!")

    check = next(
        item for item in result["checks"]
        if item["id"] == "uppercase"
    )

    assert check["passed"] is False


def test_password_without_digits_fails():
    result = check_password_policy("Abcdefghijkl!")

    check = next(
        item for item in result["checks"]
        if item["id"] == "digits"
    )

    assert check["passed"] is False


def test_password_without_symbols_fails():
    result = check_password_policy("Abcdefghijkl12")

    check = next(
        item for item in result["checks"]
        if item["id"] == "symbols"
    )

    assert check["passed"] is False


def test_common_password_fails_policy():
    result = check_password_policy("password123")

    check = next(
        item for item in result["checks"]
        if item["id"] == "not_common"
    )

    assert check["passed"] is False


def test_predictable_sequence_fails_policy():
    result = check_password_policy("Abcd1234!Xyz")

    check = next(
        item for item in result["checks"]
        if item["id"] == "no_sequences"
    )

    assert check["passed"] is False


def test_keyboard_pattern_fails_policy():
    result = check_password_policy("Qwerty!A123456")

    check = next(
        item for item in result["checks"]
        if item["id"] == "no_keyboard_patterns"
    )

    assert check["passed"] is False


def test_repetition_fails_policy():
    result = check_password_policy("Abc!1111defG")

    check = next(
        item for item in result["checks"]
        if item["id"] == "no_repetitions"
    )

    assert check["passed"] is False


def test_predictable_prefix_fails_policy():
    result = check_password_policy("Password!Abc123")

    check = next(
        item for item in result["checks"]
        if item["id"] == "no_predictable_patterns"
    )

    assert check["passed"] is False


def test_failed_checks_have_recommendations():
    result = check_password_policy("password123")

    assert result["failed_checks"] > 0
    assert len(result["recommendations"]) == result["failed_checks"]


def test_check_counts_are_consistent():
    result = check_password_policy("password123")

    assert (
        result["passed_checks"] + result["failed_checks"]
        == result["total_checks"]
    )


def test_password_is_not_returned():
    password = "Synthetic!Password987"
    result = check_password_policy(password)

    assert password not in str(result)


def test_privacy_flags_are_false():
    result = check_password_policy("Violet!Cedar#74Moon")

    assert result["privacy"] == {
        "password_returned": False,
        "password_stored": False,
        "password_logged": False,
    }


def test_non_string_password_raises_type_error():
    with pytest.raises(TypeError):
        check_password_policy(123456)


def test_empty_password_is_evaluated_without_crashing():
    result = check_password_policy("")

    assert result["compliant"] is False
    assert result["failed_checks"] > 0