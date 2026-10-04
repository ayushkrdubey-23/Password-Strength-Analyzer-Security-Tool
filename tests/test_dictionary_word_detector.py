"""Tests for local dictionary-word detection."""

import pytest

from backend.services.dictionary_word_detector import (
    detect_dictionary_words
)


def test_detect_dictionary_word():
    result = detect_dictionary_words("Winter2026!")

    assert result["detected"] is True


def test_detect_word_case_insensitively():
    result = detect_dictionary_words("WELCOME123!")

    assert result["detected"] is True


def test_detect_word_inside_longer_password():
    result = detect_dictionary_words("MySecretCombination938!")

    assert result["detected"] is True


def test_detect_word_surrounded_by_symbols():
    result = detect_dictionary_words("##Dragon##938!")

    assert result["detected"] is True


def test_detect_word_surrounded_by_numbers():
    result = detect_dictionary_words("123Sunshine456!")

    assert result["detected"] is True


def test_unrelated_password_not_detected():
    result = detect_dictionary_words("XyZ!7391Qv#")

    assert result["detected"] is False


def test_empty_password():
    result = detect_dictionary_words("")

    assert result["detected"] is False


def test_invalid_password_type():
    with pytest.raises(TypeError):
        detect_dictionary_words(None)


def test_custom_dictionary(tmp_path):
    dataset = tmp_path / "words.txt"

    dataset.write_text(
        "nebula\n"
        "galaxy\n",
        encoding="utf-8"
    )

    result = detect_dictionary_words(
        "MyNebula2026!",
        dictionary_path=dataset
    )

    assert result["detected"] is True


def test_custom_dictionary_is_case_insensitive(tmp_path):
    dataset = tmp_path / "words.txt"

    dataset.write_text(
        "nebula\n",
        encoding="utf-8"
    )

    result = detect_dictionary_words(
        "NEBULA123!",
        dictionary_path=dataset
    )

    assert result["detected"] is True


def test_short_dictionary_entries_are_ignored(tmp_path):
    dataset = tmp_path / "words.txt"

    dataset.write_text(
        "cat\n"
        "dog\n"
        "apple\n",
        encoding="utf-8"
    )

    result = detect_dictionary_words(
        "cat123!",
        dictionary_path=dataset
    )

    assert result["detected"] is False


def test_missing_dictionary_raises_error(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        detect_dictionary_words(
            "Winter2026!",
            dictionary_path=missing_file
        )


def test_matched_word_is_not_returned():
    password = "Winter2026!"

    result = detect_dictionary_words(password)

    assert password not in str(result)
    assert "winter" not in str(result).casefold()


def test_result_contains_only_pattern_metadata():
    result = detect_dictionary_words("Dragon2026!")

    for pattern in result["patterns"]:

        assert set(pattern.keys()) == {
            "type",
            "length"
        }

        assert pattern["type"] == "dictionary_word"


def test_findings_and_suggestions_are_lists():
    result = detect_dictionary_words("Winter2026!")

    assert isinstance(result["findings"], list)
    assert isinstance(result["suggestions"], list)


def test_no_findings_when_no_word_is_detected():
    result = detect_dictionary_words("XyZ!7391Qv#")

    assert result["findings"] == []
    assert result["suggestions"] == []
    