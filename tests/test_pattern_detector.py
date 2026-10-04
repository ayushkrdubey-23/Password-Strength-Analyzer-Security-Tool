
import pytest

from backend.services.pattern_detector import (
    detect_sequences,
    detect_keyboard_patterns
)


# -------------------------------
# Sequence detection tests
# -------------------------------

@pytest.mark.parametrize(
    "password, expected_type",
    [
        ("1234", "ascending_numeric"),
        ("567890", "ascending_numeric"),
        ("9876", "descending_numeric"),
        ("abcd", "ascending_alphabetic"),
        ("BCDE", "ascending_alphabetic"),
        ("dcba", "descending_alphabetic"),
        ("987654321", "descending_numeric"),
    ]
)
def test_detects_sequences(password, expected_type):
    result = detect_sequences(password)

    assert result["detected"] is True
    assert any(
        pattern["type"] == expected_type
        for pattern in result["patterns"]
    )


@pytest.mark.parametrize(
    "password",
    [
        "1357",
        "aceg",
        "a1b2c3",
        "hello",
        "x9z2",
        "",
        "12-34",
        "ab-cd"
    ]
)
def test_does_not_detect_non_sequences(password):
    result = detect_sequences(password)

    assert result["detected"] is False
    assert result["patterns"] == []


def test_sequence_length_is_reported():
    result = detect_sequences("12345")

    assert result["patterns"][0]["length"] == 5


def test_sequence_detection_does_not_return_password():
    password = "123456"

    result = detect_sequences(password)

    assert password not in str(result)


def test_sequence_detection_does_not_modify_input():
    password = "abc12345"

    detect_sequences(password)

    assert password == "abc12345"


def test_sequence_detector_rejects_non_string():
    with pytest.raises(TypeError):
        detect_sequences(123456)


# -------------------------------
# Keyboard pattern tests
# -------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "qwerty",
        "asdf",
        "zxcv",
        "QWERTY123",
        "ytrewq",
        "fdsa",
        "vcxz"
    ]
)
def test_detects_keyboard_patterns(password):
    result = detect_keyboard_patterns(password)

    assert result["detected"] is True
    assert len(result["patterns"]) > 0


@pytest.mark.parametrize(
    "password",
    [
        "hello",
        "python2026",
        "secure!pass",
        "random987",
        "",
        "13579"
    ]
)
def test_does_not_detect_normal_password_patterns(password):
    result = detect_keyboard_patterns(password)

    assert result["detected"] is False


def test_detects_vertical_keyboard_pattern():
    result = detect_keyboard_patterns("qaz123")

    assert result["detected"] is True
    assert any(
        pattern["type"] == "vertical_or_diagonal_keyboard_walk"
        for pattern in result["patterns"]
    )


def test_keyboard_detection_does_not_return_password():
    password = "qwerty"

    result = detect_keyboard_patterns(password)

    assert password not in str(result)


def test_keyboard_detector_rejects_non_string():
    with pytest.raises(TypeError):
        detect_keyboard_patterns(None)


def test_keyboard_detection_does_not_modify_input():
    password = "QWERTY123"

    detect_keyboard_patterns(password)

    assert password == "QWERTY123"
    