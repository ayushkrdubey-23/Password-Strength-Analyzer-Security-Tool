
"""
Detect predictable password prefixes, suffixes, years and dates.

Privacy:
- Does not store passwords.
- Does not print or log passwords.
- Does not return matched password characters.
"""

import re
from datetime import datetime


COMMON_PREFIXES = (
    "password",
    "admin",
    "welcome",
    "user",
    "login",
    "letmein",
    "hello",
)

COMMON_SUFFIXES = (
    "password",
    "admin",
    "welcome",
    "user",
    "login",
    "letmein",
    "hello",
)


def _is_valid_date(value: str) -> bool:
    """Check supported eight-digit date formats."""
    formats = ("%Y%m%d", "%d%m%Y", "%m%d%Y")

    for date_format in formats:
        try:
            datetime.strptime(value, date_format)
            return True
        except ValueError:
            continue

    return False


def detect_predictable_patterns(password: str) -> dict:
    """
    Detect common prefixes, suffixes, years and date patterns.

    Years from 1900 to 2099 are flagged.
    Eight-digit dates are checked for validity.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    normalized = password.casefold()
    patterns = []

    # Common predictable prefixes.
    for prefix in COMMON_PREFIXES:
        if normalized.startswith(prefix):
            patterns.append({
                "type": "common_prefix",
                "length": len(prefix)
            })
            break

    # Common predictable suffixes.
    for suffix in COMMON_SUFFIXES:
        if normalized.endswith(suffix):
            patterns.append({
                "type": "common_suffix",
                "length": len(suffix)
            })
            break

    # Detect years between 1900 and 2099.
    years = re.findall(r"(?<!\d)(?:19|20)\d{2}(?!\d)", password)

    if years:
        patterns.append({
            "type": "year_pattern",
            "length": 4
        })

    # Detect valid eight-digit dates.
    eight_digit_values = re.findall(r"(?<!\d)\d{8}(?!\d)", password)

    if any(_is_valid_date(value) for value in eight_digit_values):
        patterns.append({
            "type": "date_pattern",
            "length": 8
        })

    # Detect dates with common separators:
    # DD-MM-YYYY, DD/MM/YYYY, YYYY-MM-DD, etc.
    separated_dates = re.findall(
        r"(?<!\d)(?:\d{2}[-/.]\d{2}[-/.]\d{4}"
        r"|\d{4}[-/.]\d{2}[-/.]\d{2})(?!\d)",
        password
    )

    valid_separated_date = False

    for value in separated_dates:
        normalized_date = re.sub(r"[-/.]", "", value)

        if _is_valid_date(normalized_date):
            valid_separated_date = True
            break

    if valid_separated_date:
        patterns.append({
            "type": "date_pattern",
            "length": 8
        })

    # Remove duplicate pattern entries.
    unique_patterns = []
    seen = set()

    for pattern in patterns:
        key = (pattern["type"], pattern["length"])

        if key not in seen:
            seen.add(key)
            unique_patterns.append(pattern)

    findings = []

    if unique_patterns:
        findings.append(
            "Predictable password prefixes, suffixes, years "
            "or date patterns were detected."
        )

    suggestions = []

    detected_types = {
        pattern["type"] for pattern in unique_patterns
    }

    if "common_prefix" in detected_types:
        suggestions.append(
            "Avoid starting passwords with predictable words "
            "such as common account-related terms."
        )

    if "common_suffix" in detected_types:
        suggestions.append(
            "Avoid ending passwords with common predictable words."
        )

    if "year_pattern" in detected_types:
        suggestions.append(
            "Avoid adding easily guessed years to passwords."
        )

    if "date_pattern" in detected_types:
        suggestions.append(
            "Avoid using birthdays or other predictable date formats."
        )

    return {
        "detected": bool(unique_patterns),
        "patterns": unique_patterns,
        "findings": findings,
        "suggestions": suggestions
    }