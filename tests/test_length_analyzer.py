
import pytest

from backend.services.length_analyzer import analyze_length


def test_empty_password():
    result = analyze_length("")

    assert result["length"] == 0
    assert result["band"] == "EMPTY"


def test_one_character_password():
    result = analyze_length("a")

    assert result["length"] == 1
    assert result["band"] == "VERY_SHORT"


def test_seven_character_password():
    result = analyze_length("abcdefg")

    assert result["band"] == "VERY_SHORT"


def test_eight_character_password():
    result = analyze_length("abcdefgh")

    assert result["band"] == "SHORT"


def test_eleven_character_password():
    result = analyze_length("abcdefghijk")

    assert result["band"] == "SHORT"


def test_twelve_character_password():
    result = analyze_length("abcdefghijkl")

    assert result["band"] == "BETTER_LENGTH"


def test_fifteen_character_password():
    result = analyze_length("abcdefghijklmno")

    assert result["band"] == "BETTER_LENGTH"


def test_sixteen_character_password():
    result = analyze_length("abcdefghijklmnop")

    assert result["band"] == "STRONG_LENGTH"


def test_long_repeated_password():
    result = analyze_length("a" * 20)

    assert result["length"] == 20
    assert result["band"] == "STRONG_LENGTH"


def test_invalid_password_type():
    with pytest.raises(TypeError):
        analyze_length(None)


def test_password_is_not_returned():
    result = analyze_length("SyntheticDemo123!")

    assert "password" not in result
    assert "SyntheticDemo123!" not in str(result)
    