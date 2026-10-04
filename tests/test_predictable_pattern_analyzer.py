
import pytest

from backend.services.predictable_pattern_analyzer import (
    detect_predictable_patterns
)


# -----------------------------------
# Common prefix tests
# -----------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "Password123!",
        "admin@456",
        "Welcome2026",
        "USER#123",
        "LoginSecure9"
    ]
)
def test_detects_common_prefixes(password):
    result = detect_predictable_patterns(password)

    assert any(
        pattern["type"] == "common_prefix"
        for pattern in result["patterns"]
    )


# -----------------------------------
# Common suffix tests
# -----------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "SecurePassword",
        "StrongAdmin",
        "MyWelcome",
        "SafeLogin"
    ]
)
def test_detects_common_suffixes(password):
    result = detect_predictable_patterns(password)

    assert any(
        pattern["type"] == "common_suffix"
        for pattern in result["patterns"]
    )


# -----------------------------------
# Year detection tests
# -----------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "Ayush2026!",
        "Secure1999",
        "Welcome2000",
        "Test2099"
    ]
)
def test_detects_year_patterns(password):
    result = detect_predictable_patterns(password)

    assert any(
        pattern["type"] == "year_pattern"
        for pattern in result["patterns"]
    )


def test_does_not_detect_year_outside_supported_range():
    result = detect_predictable_patterns("Secure1899!")

    assert not any(
        pattern["type"] == "year_pattern"
        for pattern in result["patterns"]
    )


# -----------------------------------
# Date detection tests
# -----------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "12052026",
        "20260512",
        "12-05-2026",
        "2026-05-12",
        "12/05/2026",
        "2026.05.12"
    ]
)
def test_detects_valid_date_patterns(password):
    result = detect_predictable_patterns(password)

    assert any(
        pattern["type"] == "date_pattern"
        for pattern in result["patterns"]
    )


def test_does_not_detect_invalid_date():
    result = detect_predictable_patterns("32132026")

    assert not any(
        pattern["type"] == "date_pattern"
        for pattern in result["patterns"]
    )


# -----------------------------------
# Negative tests
# -----------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "Xy!7mK#9pL",
        "BlueTiger!83",
        "RandomPhrase#",
        "SecureCode!57",
        "",
        "StrongPass#"
    ]
)
def test_does_not_detect_unlisted_patterns(password):
    result = detect_predictable_patterns(password)

    assert result["detected"] is False


# -----------------------------------
# Privacy and validation tests
# -----------------------------------

def test_result_does_not_return_password():
    password = "Welcome2026"

    result = detect_predictable_patterns(password)

    assert password not in str(result)


def test_detection_does_not_modify_input():
    password = "Password123!"

    detect_predictable_patterns(password)

    assert password == "Password123!"


def test_rejects_non_string_input():
    with pytest.raises(TypeError):
        detect_predictable_patterns(123456)


def test_returns_expected_result_structure():
    result = detect_predictable_patterns("SecurePassword")

    assert set(result.keys()) == {
        "detected",
        "patterns",
        "findings",
        "suggestions"
    }


def test_detects_multiple_pattern_types():
    result = detect_predictable_patterns("Welcome2026")

    detected_types = {
        pattern["type"] for pattern in result["patterns"]
    }

    assert "common_prefix" in detected_types
    assert "year_pattern" in detected_types
    