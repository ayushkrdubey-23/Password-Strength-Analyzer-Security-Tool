
"""
Detect repeated characters and repeated substrings.

Privacy:
- Does not store passwords.
- Does not print or log passwords.
- Does not return matched password characters.
"""


def detect_repetitions(password: str) -> dict:
    """
    Detect consecutive repeated characters and adjacent repeated
    substrings.

    Rules:
    - A character repeated at least 3 times is flagged.
    - A substring of length 2 to 6 repeated at least twice
      consecutively is flagged.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    patterns = []

    # Detect consecutive repeated characters.
    index = 0

    while index < len(password):
        end = index + 1

        while end < len(password) and password[end] == password[index]:
            end += 1

        run_length = end - index

        if run_length >= 3:
            patterns.append({
                "type": "repeated_character",
                "length": run_length
            })

        index = end

    # Detect repeated adjacent substrings.
    # Substring lengths range from 2 to 6.
    for unit_length in range(2, min(6, len(password) // 2) + 1):
        index = 0

        while index + (2 * unit_length) <= len(password):
            unit = password[index:index + unit_length]
            end = index + unit_length
            repetitions = 1

            while (
                end + unit_length <= len(password)
                and password[end:end + unit_length] == unit
            ):
                repetitions += 1
                end += unit_length

            if repetitions >= 2:
                patterns.append({
                    "type": "repeated_substring",
                    "length": unit_length * repetitions
                })

                # Skip the detected repeated block.
                index = end
            else:
                index += 1

    # Remove duplicate findings.
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
            "Repeated characters or substrings were detected."
        )

    suggestions = []

    if unique_patterns:
        suggestions.append(
            "Avoid repeating the same characters or short sequences. "
            "Use a more varied and unpredictable combination."
        )

    return {
        "detected": bool(unique_patterns),
        "patterns": unique_patterns,
        "findings": findings,
        "suggestions": suggestions
    }
