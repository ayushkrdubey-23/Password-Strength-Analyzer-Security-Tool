
"""
Password Length Analyzer

Evaluates password length using configurable
educational categories.

Length alone does not determine password security.
"""


def analyze_length(password):
    """
    Analyze password length.

    Args:
        password (str): Password submitted for analysis.

    Returns:
        dict: Length metrics and security findings.

    Privacy:
        The submitted password is never returned,
        stored, or logged.
    """

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    length = len(password)

    if length == 0:
        band = "EMPTY"
        assessment = "No password entered."

        findings = [
            "No password has been entered."
        ]

        suggestions = [
            "Enter a password to begin the analysis."
        ]

    elif length < 8:
        band = "VERY_SHORT"
        assessment = "Very short password."

        findings = [
            "Password length is below 8 characters."
        ]

        suggestions = [
            "Use a longer password or passphrase."
        ]

    elif length <= 11:
        band = "SHORT"
        assessment = "Short password."

        findings = [
            "Password length is between 8 and 11 characters."
        ]

        suggestions = [
            "Consider increasing the password length."
        ]

    elif length <= 15:
        band = "BETTER_LENGTH"
        assessment = "Better length contribution."

        findings = []

        suggestions = [
            "Consider using 16 or more characters for "
            "a stronger length contribution."
        ]

    else:
        band = "STRONG_LENGTH"
        assessment = "Strong length contribution."

        findings = []

        suggestions = []

    return {
        "length": length,
        "band": band,
        "assessment": assessment,
        "findings": findings,
        "suggestions": suggestions
    }