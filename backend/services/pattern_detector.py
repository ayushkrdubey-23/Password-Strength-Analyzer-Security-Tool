
"""
Detect predictable sequences and keyboard patterns.

Privacy:
- Does not store passwords.
- Does not print or log passwords.
- Does not return matched password characters.
"""


def _find_consecutive_runs(password: str) -> list:
    """Find ascending or descending numeric/alphabetic runs."""
    runs = []
    index = 0

    while index < len(password):
        current = password[index]

        if current.isascii() and current.isdigit():
            category = "numeric"
            value = ord(current)
        elif current.isascii() and current.isalpha():
            category = "alphabetic"
            value = ord(current.lower())
        else:
            index += 1
            continue

        end = index + 1
        direction = None

        while end < len(password):
            next_char = password[end]

            if category == "numeric":
                if not (next_char.isascii() and next_char.isdigit()):
                    break
                next_value = ord(next_char)
            else:
                if not (next_char.isascii() and next_char.isalpha()):
                    break
                next_value = ord(next_char.lower())

            difference = next_value - value

            if direction is None:
                if difference not in (1, -1):
                    break
                direction = difference
            elif difference != direction:
                break

            value = next_value
            end += 1

        run_length = end - index

        if direction is not None and run_length >= 4:
            if category == "numeric":
                pattern_type = (
                    "ascending_numeric"
                    if direction == 1
                    else "descending_numeric"
                )
            else:
                pattern_type = (
                    "ascending_alphabetic"
                    if direction == 1
                    else "descending_alphabetic"
                )

            runs.append({
                "type": pattern_type,
                "length": run_length
            })

        index = max(end, index + 1)

    return runs


def detect_sequences(password: str) -> dict:
    """Detect consecutive numeric and alphabetic sequences."""
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    patterns = _find_consecutive_runs(password)

    findings = []

    if patterns:
        findings.append(
            "Predictable consecutive character sequence detected."
        )

    suggestions = []

    if patterns:
        suggestions.append(
            "Avoid consecutive numbers or alphabetic sequences. "
            "Use a longer, less predictable combination."
        )

    return {
        "detected": bool(patterns),
        "patterns": patterns,
        "findings": findings,
        "suggestions": suggestions
    }


def _find_keyboard_row_matches(password: str, row: str) -> list:
    """
    Find keyboard-row substrings of at least four characters.

    Checks both forward and reverse directions.
    Returns only pattern types and lengths, never matched text.
    """
    matches = []

    for sequence in (row, row[::-1]):
        # Check the longest possible substring first.
        for length in range(len(sequence), 3, -1):
            found = False

            for start in range(len(sequence) - length + 1):
                candidate = sequence[start:start + length]

                if candidate in password:
                    matches.append({
                        "type": "horizontal_keyboard_walk",
                        "length": length
                    })
                    found = True
                    break

            if found:
                break

    return matches


def detect_keyboard_patterns(password: str) -> dict:
    """
    Detect common horizontal, vertical and diagonal keyboard walks.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    normalized = password.casefold()

    horizontal_rows = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
        "1234567890"
    ]

    additional_patterns = [
        "qaz", "wsx", "edc", "rfv", "tgb",
        "yhn", "ujm", "ik,", "ol.",
        "zaq", "xsw", "cde", "vfr", "bgt"
    ]

    patterns = []

    # Detect partial horizontal keyboard-row sequences.
    for row in horizontal_rows:
        patterns.extend(
            _find_keyboard_row_matches(normalized, row)
        )

    # Detect selected vertical and diagonal keyboard sequences.
    for sequence in additional_patterns:
        for candidate in (sequence, sequence[::-1]):
            if candidate in normalized:
                patterns.append({
                    "type": "vertical_or_diagonal_keyboard_walk",
                    "length": len(candidate)
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
            "A predictable keyboard pattern was detected."
        )

    suggestions = []

    if unique_patterns:
        suggestions.append(
            "Avoid adjacent keyboard characters and common keyboard "
            "walks. Choose a less predictable combination."
        )

    return {
        "detected": bool(unique_patterns),
        "patterns": unique_patterns,
        "findings": findings,
        "suggestions": suggestions
    }