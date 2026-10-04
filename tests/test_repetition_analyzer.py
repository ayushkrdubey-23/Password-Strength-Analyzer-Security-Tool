
import pytest

from backend.services.repetition_analyzer import detect_repetitions


# -----------------------------------
# Repeated character tests
# -----------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "aaa",
        "111",
        "aaaaaa",
        "hello!!!",
        "passssword"
    ]
)
def test_detects_repeated_characters(password):
    result = detect_repetitions(password)

    assert result["detected"] is True
    assert any(
        pattern["type"] == "repeated_character"
        for pattern in result["patterns"]
    )


def test_reports_repeated_character_length():
    result = detect_repetitions("aaaa")

    assert any(
        pattern["type"] == "repeated_character"
        and pattern["length"] == 4
        for pattern in result["patterns"]
    )


# -----------------------------------
# Repeated substring tests
# -----------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "abcabc",
        "ababab",
        "121212",
        "xyzxyz",
        "abcdabcd",
        "abcabcabc"
    ]
)
def test_detects_repeated_substrings(password):
    result = detect_repetitions(password)

    assert result["detected"] is True
    assert any(
        pattern["type"] == "repeated_substring"
        for pattern in result["patterns"]
    )


def test_reports_repeated_substring_length():
    result = detect_repetitions("abcabc")

    assert any(
        pattern["type"] == "repeated_substring"
        and pattern["length"] == 6
        for pattern in result["patterns"]
    )


# -----------------------------------
# Negative tests
# -----------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "Ayush2026!",
        "SecurePass9#",
        "python",
        "aabbcc",
        "123456",
        "",
        "abcdefghi"
    ]
)
def test_does_not_detect_unqualified_repetitions(password):
    result = detect_repetitions(password)

    assert result["detected"] is False


# -----------------------------------
# Privacy and validation tests
# -----------------------------------

def test_result_does_not_return_password():
    password = "abcabc"

    result = detect_repetitions(password)

    assert password not in str(result)


def test_result_does_not_modify_password():
    password = "abcabc"

    detect_repetitions(password)

    assert password == "abcabc"


def test_rejects_non_string_input():
    with pytest.raises(TypeError):
        detect_repetitions(123456)


def test_returns_expected_result_structure():
    result = detect_repetitions("StrongPassword123!")

    assert set(result.keys()) == {
        "detected",
        "patterns",
        "findings",
        "suggestions"
    }