"""
Central Password Analysis Engine.

Integrates:
1. Password length analysis
2. Character diversity analysis
3. Common password detection
4. Numeric/alphabetic sequence detection
5. Keyboard pattern detection
6. Repeated character and substring detection
7. Predictable prefix, suffix, year and date detection
8. Educational theoretical entropy estimation
9. Dictionary word detection

The strength score is an educational heuristic, not a
cryptographic measurement.

Privacy:
- Never returns the submitted password.
- Does not store or log submitted passwords.
- Does not make external requests.
"""

from backend.services.length_analyzer import analyze_length
from backend.services.character_analyzer import analyze_characters
from backend.services.common_password_checker import is_common_password

from backend.services.pattern_detector import (
    detect_sequences,
    detect_keyboard_patterns
)

from backend.services.repetition_analyzer import detect_repetitions

from backend.services.predictable_pattern_analyzer import (
    detect_predictable_patterns
)

from backend.services.entropy_estimator import estimate_entropy

from backend.services.dictionary_word_detector import (
    detect_dictionary_words
)


def _calculate_strength_score(
    length_result: dict,
    character_result: dict,
    common_password: bool,
    sequence_result: dict,
    keyboard_result: dict,
    repetition_result: dict,
    predictable_result: dict
) -> int:
    """
    Calculate an educational password strength score.

    Maximum positive points:
    - Length: 50
    - Character diversity: 40

    Predictable patterns reduce the score.

    Entropy and dictionary-word findings are deliberately
    excluded from this formula to preserve existing scoring.
    """

    password_length = length_result["length"]

    # Length contribution.
    if password_length == 0:
        length_points = 0
    elif password_length < 8:
        length_points = 10
    elif password_length <= 11:
        length_points = 25
    elif password_length <= 15:
        length_points = 35
    else:
        length_points = 50

    # Diversity contribution.
    character_types = character_result["character_types"]

    diversity_count = sum(
        character_types[category]
        for category in (
            "lowercase",
            "uppercase",
            "digits",
            "symbols"
        )
    )

    diversity_points = diversity_count * 10

    score = length_points + diversity_points

    # Existing security penalties.
    if common_password:
        score -= 50

    if sequence_result["detected"]:
        score -= 10

    if keyboard_result["detected"]:
        score -= 10

    if repetition_result["detected"]:
        score -= 10

    if predictable_result["detected"]:
        score -= 10

    return max(0, min(100, score))


def _get_strength_category(score: int) -> str:
    """Convert the score into an educational strength category."""

    if score < 20:
        return "VERY WEAK"
    elif score < 40:
        return "WEAK"
    elif score < 60:
        return "MODERATE"
    elif score < 80:
        return "STRONG"
    else:
        return "VERY STRONG"


def analyze_password(password: str) -> dict:
    """
    Run all password analysis modules and combine their results.

    Args:
        password: Password entered for analysis.

    Returns:
        A dictionary containing component results, score,
        strength category, findings and suggestions.

    Raises:
        TypeError: If password is not a string.
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    # Run individual analysis modules.
    length_result = analyze_length(password)

    character_result = analyze_characters(password)

    common_password = is_common_password(password)

    sequence_result = detect_sequences(password)

    keyboard_result = detect_keyboard_patterns(password)

    repetition_result = detect_repetitions(password)

    predictable_result = detect_predictable_patterns(password)

    entropy_result = estimate_entropy(password)

    dictionary_result = detect_dictionary_words(password)

    # Calculate the combined educational score.
    # Entropy and dictionary findings do not alter the formula.
    score = _calculate_strength_score(
        length_result=length_result,
        character_result=character_result,
        common_password=common_password,
        sequence_result=sequence_result,
        keyboard_result=keyboard_result,
        repetition_result=repetition_result,
        predictable_result=predictable_result
    )

    strength = _get_strength_category(score)

    # Prepare the common-password result.
    common_password_result = {
        "detected": common_password,
        "findings": [],
        "suggestions": []
    }

    if common_password:

        common_password_result["findings"].append(
            "Password matches an entry in the local common-password dataset."
        )

        common_password_result["suggestions"].append(
            "Avoid commonly used passwords. Choose a unique password "
            "or a long, randomly generated passphrase."
        )

    # Combine every component result.
    analyses = {
        "length": length_result,
        "characters": character_result,
        "common_password": common_password_result,
        "sequences": sequence_result,
        "keyboard_patterns": keyboard_result,
        "repetitions": repetition_result,
        "predictable_patterns": predictable_result,
        "entropy": entropy_result,
        "dictionary_words": dictionary_result
    }

    # Collect findings and suggestions.
    findings = []

    suggestions = []

    for result in analyses.values():

        findings.extend(result.get("findings", []))

        suggestions.extend(result.get("suggestions", []))

    # Remove duplicate messages while preserving their order.
    findings = list(dict.fromkeys(findings))

    suggestions = list(dict.fromkeys(suggestions))

    if not suggestions:

        suggestions.append(
            "Continue using unique passwords and enable multi-factor "
            "authentication wherever available."
        )

    return {
        "score": score,
        "strength": strength,
        "summary": (
            "Password analysis completed using local educational "
            "security checks."
        ),
        "analyses": analyses,
        "findings": findings,
        "suggestions": suggestions,
        "privacy": {
            "password_returned": False,
            "password_stored": False,
            "external_requests_made": False
        },
        "scoring_note": (
            "This score is an educational heuristic and is not a "
            "cryptographic guarantee of password security. The theoretical "
            "entropy estimate and dictionary-word findings are reported "
            "separately and do not affect the existing strength score."
        )
    }