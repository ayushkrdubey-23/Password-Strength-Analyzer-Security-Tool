
import pytest

from backend.services.common_password_checker import (
    is_common_password
)


def test_password_matches_dataset():
    assert is_common_password("password") is True


def test_numeric_common_password():
    assert is_common_password("123456") is True


def test_common_password_case_insensitive():
    assert is_common_password("PASSWORD") is True


def test_mixed_case_common_password():
    assert is_common_password("PaSsWoRd") is True


def test_keyboard_password():
    assert is_common_password("qwerty") is True


def test_uncommon_password_not_found():
    assert is_common_password(
        "Synthetic-Uncommon-Demo-739!"
    ) is False


def test_password_with_meaningful_space():
    assert is_common_password(" password") is False


def test_empty_password():
    assert is_common_password("") is False


def test_invalid_password_type():
    with pytest.raises(TypeError):
        is_common_password(None)


def test_missing_dataset_raises_error(tmp_path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        is_common_password(
            "password",
            dataset_path=missing_file
        )


def test_custom_dataset(tmp_path):
    dataset = tmp_path / "custom_passwords.txt"

    dataset.write_text(
        "# Test dataset\n"
        "example123\n"
        "demo456\n",
        encoding="utf-8"
    )

    assert is_common_password(
        "example123",
        dataset_path=dataset
    ) is True


def test_custom_dataset_case_insensitive(tmp_path):
    dataset = tmp_path / "custom_passwords.txt"

    dataset.write_text(
        "example123\n",
        encoding="utf-8"
    )

    assert is_common_password(
        "EXAMPLE123",
        dataset_path=dataset
    ) is True


def test_blank_dataset_entries_are_ignored(tmp_path):
    dataset = tmp_path / "blank_passwords.txt"

    dataset.write_text(
        "\n"
        "# Comment\n"
        "demo123\n"
        "\n",
        encoding="utf-8"
    )

    assert is_common_password(
        "",
        dataset_path=dataset
    ) is False


def test_submitted_password_is_not_returned():
    demo_password = "SyntheticDemo123!"

    result = is_common_password(demo_password)

    assert result is False
    assert isinstance(result, bool)


def test_submitted_password_is_not_modified():
    demo_password = " Password "

    is_common_password(demo_password)

    assert demo_password == " Password "
