"""
Password Policy Checker.

Evaluates a password against a fixed educational security policy.

Privacy:
- Does not store passwords.
- Does not print or log passwords.
- Does not return submitted password characters.
- Reuses existing local password-analysis services.
"""

from backend.services.character_analyzer import analyze_characters
from backend.services.common_password_checker import is_common_password
from backend.services.pattern_detector import (
    detect_keyboard_patterns,
    detect_sequences,
)
from backend.services.repetition_analyzer import detect_repetitions
from backend.services.predictable_pattern_analyzer import (
    detect_predictable_patterns,
)


DEFAULT_POLICY = {
    "minimum_length": 12,
    "require_lowercase": True,
    "require_uppercase": True,
    "require_digits": True,
    "require_symbols": True,
    "reject_common_passwords": True,
    "reject_sequences": True,
    "reject_keyboard_patterns": True,
    "reject_repetitions": True,
    "reject_predictable_patterns": True,
}


def check_password_policy(password):
    """
    Check a password against the default security policy.

    Args:
        password (str): Password submitted for evaluation.

    Returns:
        dict: Individual policy results and recommendations.

    Raises:
        TypeError: If password is not a string.
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    character_analysis = analyze_characters(password)
    character_types = character_analysis["character_types"]

    common_password = is_common_password(password)
    sequence_analysis = detect_sequences(password)
    keyboard_analysis = detect_keyboard_patterns(password)
    repetition_analysis = detect_repetitions(password)
    predictable_analysis = detect_predictable_patterns(password)

    checks = [
        {
            "id": "minimum_length",
            "label": "Minimum length",
            "passed": len(password) >= DEFAULT_POLICY["minimum_length"],
            "message": "Password must contain at least 12 characters.",
            "recommendation": (
                "Use at least 12 characters. A longer passphrase "
                "can provide better protection."
            ),
        },
        {
            "id": "lowercase",
            "label": "Lowercase letter",
            "passed": character_types["lowercase"],
            "message": "Include at least one lowercase letter.",
            "recommendation": "Add at least one lowercase letter.",
        },
        {
            "id": "uppercase",
            "label": "Uppercase letter",
            "passed": character_types["uppercase"],
            "message": "Include at least one uppercase letter.",
            "recommendation": "Add at least one uppercase letter.",
        },
        {
            "id": "digits",
            "label": "Number",
            "passed": character_types["digits"],
            "message": "Include at least one numeric digit.",
            "recommendation": "Add at least one number.",
        },
        {
            "id": "symbols",
            "label": "Special character",
            "passed": character_types["symbols"],
            "message": "Include at least one special character.",
            "recommendation": (
                "Add a special character, such as !, @, #, or %."
            ),
        },
        {
            "id": "not_common",
            "label": "Not a common password",
            "passed": not common_password,
            "message": "Avoid passwords found in common-password lists.",
            "recommendation": (
                "Avoid commonly used passwords and predictable variations."
            ),
        },
        {
            "id": "no_sequences",
            "label": "No predictable sequences",
            "passed": not sequence_analysis["detected"],
            "message": "Avoid consecutive numeric or alphabetic sequences.",
            "recommendation": (
                "Replace predictable consecutive sequences with "
                "less predictable characters."
            ),
        },
        {
            "id": "no_keyboard_patterns",
            "label": "No keyboard patterns",
            "passed": not keyboard_analysis["detected"],
            "message": "Avoid common keyboard walks.",
            "recommendation": (
                "Avoid adjacent keyboard patterns and keyboard walks."
            ),
        },
        {
            "id": "no_repetitions",
            "label": "No excessive repetitions",
            "passed": not repetition_analysis["detected"],
            "message": "Avoid repeated characters and adjacent substrings.",
            "recommendation": (
                "Avoid long repeated characters or repeated adjacent "
                "character groups."
            ),
        },
        {
            "id": "no_predictable_patterns",
            "label": "No predictable prefixes, suffixes or dates",
            "passed": not predictable_analysis["detected"],
            "message": "Avoid predictable words, years and date patterns.",
            "recommendation": (
                "Avoid common prefixes, suffixes, years and date patterns."
            ),
        },
    ]

    passed_checks = sum(
        1 for check in checks if check["passed"]
    )

    failed_checks = len(checks) - passed_checks

    recommendations = [
        check["recommendation"]
        for check in checks
        if not check["passed"]
    ]

    return {
        "policy_name": "Default Password Security Policy",
        "compliant": failed_checks == 0,
        "total_checks": len(checks),
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "checks": [
            {
                "id": check["id"],
                "label": check["label"],
                "passed": check["passed"],
                "message": check["message"],
            }
            for check in checks
        ],
        "recommendations": recommendations,
        "privacy": {
            "password_returned": False,
            "password_stored": False,
            "password_logged": False,
        },
        "policy_note": (
            "This is an educational policy checker. "
            "Passing these checks does not guarantee that a password "
            "is secure against every attack."
        ),
    }
