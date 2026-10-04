"""Tests for the central password analysis engine."""

import pytest

from backend.services.password_analyzer import analyze_password


def test_analyzer_returns_complete_result():
    result = analyze_password("MyUnique!Pass938")

    assert "score" in result
    assert "strength" in result
    assert "summary" in result
    assert "analyses" in result
    assert "findings" in result
    assert "suggestions" in result
    assert "privacy" in result
    assert "scoring_note" in result


def test_all_analysis_modules_are_integrated():
    result = analyze_password("MyUnique!Pass938")

    expected_modules = {
        "length",
        "characters",
        "common_password",
        "sequences",
        "keyboard_patterns",
        "repetitions",
        "predictable_patterns",
        "entropy",
        "dictionary_words"
    }

    assert set(result["analyses"].keys()) == expected_modules


def test_entropy_result_is_integrated():
    result = analyze_password("MyUnique!Pass938")

    entropy = result["analyses"]["entropy"]

    assert entropy["estimate_available"] is True
    assert entropy["estimated_bits"] > 0
    assert entropy["character_pool_size"] == 94


def test_dictionary_word_result_is_integrated():
    result = analyze_password("Winter2026!")

    dictionary_result = result["analyses"]["dictionary_words"]

    assert dictionary_result["detected"] is True


def test_dictionary_word_does_not_change_existing_score():
    result = analyze_password("MyUnique!Pass938")

    # 16 characters: 50 length points + 40 diversity points.
    # No existing scoring penalties apply to this example.
    assert result["score"] == 90


def test_entropy_does_not_change_existing_score():
    result = analyze_password("MyUnique!Pass938")

    assert result["score"] == 90


def test_common_password_is_flagged():
    result = analyze_password("password123")

    assert result["analyses"]["common_password"]["detected"] is True


def test_sequence_is_detected():
    result = analyze_password("Secure1234!")

    assert result["analyses"]["sequences"]["detected"] is True


def test_keyboard_pattern_is_detected():
    result = analyze_password("MyQwertyPass!")

    assert result["analyses"]["keyboard_patterns"]["detected"] is True


def test_repetition_is_detected():
    result = analyze_password("StrongAAA!2026")

    assert result["analyses"]["repetitions"]["detected"] is True


def test_predictable_year_is_detected():
    result = analyze_password("UniquePass2026!")

    assert any(
        pattern["type"] == "year_pattern"
        for pattern in result["analyses"]["predictable_patterns"]["patterns"]
    )


def test_empty_password_is_very_weak():
    result = analyze_password("")

    assert result["score"] == 0
    assert result["strength"] == "VERY WEAK"
    assert result["analyses"]["entropy"]["estimated_bits"] == 0.0


def test_long_diverse_password_gets_high_score():
    result = analyze_password("MyUnique!Pass938")

    assert result["score"] >= 80
    assert result["strength"] == "VERY STRONG"


def test_score_stays_within_zero_and_one_hundred():
    result = analyze_password("password123")

    assert 0 <= result["score"] <= 100


def test_strength_category_matches_score():
    result = analyze_password("MyUnique!Pass938")

    if result["score"] < 20:
        expected = "VERY WEAK"
    elif result["score"] < 40:
        expected = "WEAK"
    elif result["score"] < 60:
        expected = "MODERATE"
    elif result["score"] < 80:
        expected = "STRONG"
    else:
        expected = "VERY STRONG"

    assert result["strength"] == expected


def test_result_does_not_contain_submitted_password():
    password = "MyUnique!Pass938"

    result = analyze_password(password)

    assert password not in str(result)


def test_privacy_indicators_are_enabled():
    result = analyze_password("MyUnique!Pass938")

    assert result["privacy"] == {
        "password_returned": False,
        "password_stored": False,
        "external_requests_made": False,
    }


def test_findings_and_suggestions_are_lists():
    result = analyze_password("password123")

    assert isinstance(result["findings"], list)
    assert isinstance(result["suggestions"], list)


def test_suggestions_are_not_duplicated():
    result = analyze_password("password123")

    assert len(result["suggestions"]) == len(
        set(result["suggestions"])
    )


def test_analyzer_does_not_modify_input():
    password = "MyUnique!Pass938"

    analyze_password(password)

    assert password == "MyUnique!Pass938"


def test_rejects_non_string_input():
    with pytest.raises(TypeError):
        analyze_password(123456)


def test_rejects_none_input():
    with pytest.raises(TypeError):
        analyze_password(None)


def test_unicode_password_keeps_other_analysis_available():
    result = analyze_password("Café123!")

    assert result["analyses"]["entropy"]["estimate_available"] is False
    assert result["analyses"]["length"]["length"] == 8
    assert isinstance(result["score"], int)