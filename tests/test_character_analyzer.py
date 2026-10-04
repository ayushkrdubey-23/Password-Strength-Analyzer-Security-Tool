
import pytest

from backend.services.character_analyzer import analyze_characters


def test_lowercase_detection():
    result = analyze_characters("abcdef")

    assert result["character_types"]["lowercase"] is True
    assert result["character_types"]["uppercase"] is False


def test_uppercase_detection():
    result = analyze_characters("ABCDEF")

    assert result["character_types"]["uppercase"] is True


def test_digit_detection():
    result = analyze_characters("123456")

    assert result["character_types"]["digits"] is True


def test_symbol_detection():
    result = analyze_characters("!@#$%")

    assert result["character_types"]["symbols"] is True


def test_space_detection():
    result = analyze_characters("hello world")

    assert result["character_types"]["spaces"] is True


def test_mixed_character_detection():
    result = analyze_characters("Abc123!")

    types = result["character_types"]

    assert types["lowercase"] is True
    assert types["uppercase"] is True
    assert types["digits"] is True
    assert types["symbols"] is True


def test_unique_character_count():
    result = analyze_characters("aabbcc")

    assert result["unique_character_count"] == 3


def test_character_type_count():
    result = analyze_characters("Abc123!")

    assert result["character_type_count"] == 4


def test_unique_character_ratio():
    result = analyze_characters("aabbcc")

    assert result["unique_character_ratio"] == 0.5


def test_empty_password():
    result = analyze_characters("")

    assert result["length"] == 0
    assert result["unique_character_count"] == 0
    assert result["character_type_count"] == 0
    assert result["unique_character_ratio"] == 0.0


def test_unicode_characters():
    result = analyze_characters("Abc123é")

    assert result["character_types"]["lowercase"] is True
    assert result["character_types"]["uppercase"] is True


def test_invalid_password_type():
    with pytest.raises(TypeError):
        analyze_characters(None)


def test_password_is_not_returned():
    result = analyze_characters("SyntheticDemo123!")

    assert "password" not in result
    assert "SyntheticDemo123!" not in str(result)
    