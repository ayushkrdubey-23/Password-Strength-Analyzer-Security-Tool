
"""Privacy and data-leakage regression tests.

These tests use synthetic demo values only.
"""

import sqlite3
from pathlib import Path

import pytest

from backend import create_app


SYNTHETIC_PASSWORD = "Privacy-Regression-Demo-938!"
SYNTHETIC_HASH_PASSWORD = "Argon2-Privacy-Demo-2026!"


@pytest.fixture
def privacy_client(tmp_path):
    """Create an isolated app and SQLite database for privacy tests."""

    app = create_app()

    database_path = tmp_path / "privacy_test.db"

    app.config.update({
        "TESTING": True,
        "RATELIMIT_ENABLED": False,
        "DATABASE_PATH": str(database_path)
    })

    with app.test_client() as client:
        yield client, database_path


def read_database_contents(database_path):
    """Return all SQLite table names, columns, and stored row values."""

    if not database_path.exists():
        return {}

    connection = sqlite3.connect(str(database_path))

    try:
        table_names = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

        database_contents = {}

        for (table_name,) in table_names:
            columns = connection.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()

            rows = connection.execute(
                f'SELECT * FROM "{table_name}"'
            ).fetchall()

            database_contents[table_name] = {
                "columns": [column[1] for column in columns],
                "rows": rows
            }

        return database_contents

    finally:
        connection.close()


def test_analyzer_does_not_return_password_or_save_history(privacy_client):
    client, _ = privacy_client

    response = client.post(
        "/api/analyze",
        json={"password": SYNTHETIC_PASSWORD}
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert SYNTHETIC_PASSWORD not in response.get_data(as_text=True)

    history_response = client.get("/api/history")

    assert history_response.status_code == 200
    assert history_response.json["total_records"] == 0


def test_analyzer_password_is_not_in_request_url(privacy_client):
    client, _ = privacy_client

    response = client.post(
        "/api/analyze",
        json={"password": SYNTHETIC_PASSWORD}
    )

    assert response.status_code == 200
    assert SYNTHETIC_PASSWORD not in response.request.path
    assert "password=" not in response.request.query_string.decode(
        "utf-8"
    )


def test_analyzer_error_does_not_echo_sensitive_input(privacy_client):
    client, _ = privacy_client

    response = client.post(
        "/api/analyze",
        json={
            "password": None,
            "extra_demo_value": SYNTHETIC_PASSWORD
        }
    )

    assert response.status_code == 400
    assert SYNTHETIC_PASSWORD not in response.get_data(as_text=True)


def test_history_rejects_password_and_hash_fields(privacy_client):
    client, _ = privacy_client

    metadata = {
        "score": 90,
        "strength": "VERY STRONG",
        "findings_count": 0,
        "character_types_count": 4,
        "analysis_completed": True,
        "password": SYNTHETIC_PASSWORD,
        "password_hash": "synthetic-demo-hash"
    }

    response = client.post(
        "/api/history",
        json=metadata
    )

    assert response.status_code == 400
    assert SYNTHETIC_PASSWORD not in response.get_data(as_text=True)
    assert "synthetic-demo-hash" not in response.get_data(as_text=True)


def test_argon2_demo_does_not_persist_password_or_hash(privacy_client):
    client, database_path = privacy_client

    hash_response = client.post(
        "/api/hash-demo/hash",
        json={"password": SYNTHETIC_HASH_PASSWORD}
    )

    assert hash_response.status_code == 200

    encoded_hash = hash_response.json["encoded_hash"]

    verify_response = client.post(
        "/api/hash-demo/verify",
        json={
            "password": SYNTHETIC_HASH_PASSWORD,
            "encoded_hash": encoded_hash
        }
    )

    assert verify_response.status_code == 200
    assert verify_response.json["matches"] is True

    # Accessing history initializes the database if needed.
    history_response = client.get("/api/history")

    assert history_response.status_code == 200
    assert history_response.json["total_records"] == 0

    database_contents = read_database_contents(database_path)
    database_text = repr(database_contents)

    assert SYNTHETIC_HASH_PASSWORD not in database_text
    assert encoded_hash not in database_text


def test_generated_password_is_not_saved_in_history(privacy_client):
    client, database_path = privacy_client

    generator_response = client.post(
        "/api/generate",
        json={
            "length": 24,
            "include_lowercase": True,
            "include_uppercase": True,
            "include_digits": True,
            "include_symbols": True
        }
    )

    assert generator_response.status_code == 200

    generated_password = generator_response.json["data"]["password"]

    assert generated_password
    assert len(generated_password) == 24

    history_response = client.get("/api/history")

    assert history_response.status_code == 200
    assert history_response.json["total_records"] == 0

    database_contents = read_database_contents(database_path)

    assert generated_password not in repr(database_contents)


def test_history_database_has_only_approved_columns(privacy_client):
    client, database_path = privacy_client

    metadata = {
        "score": 90,
        "strength": "VERY STRONG",
        "findings_count": 0,
        "character_types_count": 4,
        "analysis_completed": True
    }

    response = client.post(
        "/api/history",
        json=metadata
    )

    assert response.status_code == 201

    database_contents = read_database_contents(database_path)

    assert "analysis_history" in database_contents

    columns = set(
        database_contents["analysis_history"]["columns"]
    )

    expected_columns = {
        "id",
        "created_at",
        "score",
        "strength",
        "findings_count",
        "character_types_count",
        "analysis_completed"
    }

    assert columns == expected_columns


def test_history_database_does_not_contain_password_values(privacy_client):
    client, database_path = privacy_client

    metadata = {
        "score": 75,
        "strength": "STRONG",
        "findings_count": 1,
        "character_types_count": 4,
        "analysis_completed": True
    }

    response = client.post(
        "/api/history",
        json=metadata
    )

    assert response.status_code == 201

    database_contents = read_database_contents(database_path)
    database_text = repr(database_contents)

    assert SYNTHETIC_PASSWORD not in database_text
    assert SYNTHETIC_HASH_PASSWORD not in database_text
    assert "password_hash" not in database_text


def test_frontend_does_not_use_browser_storage():
    project_root = Path(__file__).resolve().parents[1]
    javascript_path = project_root / "frontend" / "js" / "app.js"

    javascript = javascript_path.read_text(encoding="utf-8")

    assert "localStorage" not in javascript
    assert "sessionStorage" not in javascript


def test_frontend_sends_analysis_password_using_post_body():
    project_root = Path(__file__).resolve().parents[1]
    javascript_path = project_root / "frontend" / "js" / "app.js"

    javascript = javascript_path.read_text(encoding="utf-8")

    assert 'fetch("/api/analyze"' in javascript
    assert 'method: "POST"' in javascript
    assert "JSON.stringify({" in javascript
    assert "password: password" in javascript


def test_frontend_history_metadata_does_not_include_password():
    project_root = Path(__file__).resolve().parents[1]
    javascript_path = project_root / "frontend" / "js" / "app.js"

    javascript = javascript_path.read_text(encoding="utf-8")

    start_marker = "latestHistoryMetadata = {"
    start = javascript.find(start_marker)

    assert start != -1

    end = javascript.find("};", start)

    assert end != -1

    metadata_block = javascript[start:end]

    expected_fields = [
        "score:",
        "strength:",
        "findings_count:",
        "character_types_count:",
        "analysis_completed:"
    ]

    for field in expected_fields:
        assert field in metadata_block

    assert "password:" not in metadata_block
    assert "encoded_hash:" not in metadata_block


def test_frontend_does_not_log_passwords_to_console():
    project_root = Path(__file__).resolve().parents[1]
    javascript_path = project_root / "frontend" / "js" / "app.js"

    javascript = javascript_path.read_text(encoding="utf-8")

    assert "console.log(" not in javascript
    assert "console.error(" not in javascript
    assert "console.warn(" not in javascript
    