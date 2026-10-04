"""Tests for privacy-first analysis history API."""

import sqlite3

import pytest

from backend import create_app


@pytest.fixture
def history_client(tmp_path):
    """Create an isolated test application and database."""

    app = create_app()

    app.config.update({
        "TESTING": True,
        "DATABASE_PATH": str(
            tmp_path / "test_history.db"
        )
    })

    with app.test_client() as client:
        yield client, app.config["DATABASE_PATH"]


def valid_metadata():
    """Return synthetic, non-sensitive test metadata."""

    return {
        "score": 90,
        "strength": "VERY STRONG",
        "findings_count": 0,
        "character_types_count": 4,
        "analysis_completed": True
    }


def test_save_history_success(history_client):
    client, _ = history_client

    response = client.post(
        "/api/history",
        json=valid_metadata()
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True
    assert data["data"]["score"] == 90


def test_history_is_not_created_automatically(history_client):
    client, _ = history_client

    response = client.get("/api/history")

    assert response.status_code == 200
    assert response.get_json()["total_records"] == 0


def test_get_saved_history(history_client):
    client, _ = history_client

    client.post("/api/history", json=valid_metadata())

    response = client.get("/api/history")

    assert response.status_code == 200
    assert response.get_json()["total_records"] == 1


def test_reject_password_field(history_client):
    client, _ = history_client

    metadata = valid_metadata()
    metadata["password"] = "SyntheticDemo123!"

    response = client.post("/api/history", json=metadata)

    assert response.status_code == 400


def test_reject_password_hash_field(history_client):
    client, _ = history_client

    metadata = valid_metadata()
    metadata["password_hash"] = "synthetic-hash"

    response = client.post("/api/history", json=metadata)

    assert response.status_code == 400


def test_reject_missing_fields(history_client):
    client, _ = history_client

    response = client.post(
        "/api/history",
        json={"score": 90}
    )

    assert response.status_code == 400


def test_reject_invalid_score(history_client):
    client, _ = history_client

    metadata = valid_metadata()
    metadata["score"] = 101

    response = client.post("/api/history", json=metadata)

    assert response.status_code == 400


def test_reject_boolean_score(history_client):
    client, _ = history_client

    metadata = valid_metadata()
    metadata["score"] = True

    response = client.post("/api/history", json=metadata)

    assert response.status_code == 400


def test_reject_incorrect_strength_category(history_client):
    client, _ = history_client

    metadata = valid_metadata()
    metadata["strength"] = "WEAK"

    response = client.post("/api/history", json=metadata)

    assert response.status_code == 400


def test_reject_invalid_findings_count(history_client):
    client, _ = history_client

    metadata = valid_metadata()
    metadata["findings_count"] = -1

    response = client.post("/api/history", json=metadata)

    assert response.status_code == 400


def test_reject_invalid_character_types_count(history_client):
    client, _ = history_client

    metadata = valid_metadata()
    metadata["character_types_count"] = 5

    response = client.post("/api/history", json=metadata)

    assert response.status_code == 400


def test_reject_non_boolean_completion_status(history_client):
    client, _ = history_client

    metadata = valid_metadata()
    metadata["analysis_completed"] = 1

    response = client.post("/api/history", json=metadata)

    assert response.status_code == 400


def test_reject_non_json_request(history_client):
    client, _ = history_client

    response = client.post(
        "/api/history",
        data="not-json",
        content_type="text/plain"
    )

    assert response.status_code == 415


def test_clear_history(history_client):
    client, _ = history_client

    client.post("/api/history", json=valid_metadata())

    response = client.delete("/api/history")

    assert response.status_code == 200
    assert response.get_json()["deleted_records"] == 1

    history = client.get("/api/history").get_json()

    assert history["total_records"] == 0


def test_database_does_not_have_password_columns(history_client):
    client, database_path = history_client

    client.post("/api/history", json=valid_metadata())

    connection = sqlite3.connect(database_path)

    try:
        columns = connection.execute(
            "PRAGMA table_info(analysis_history)"
        ).fetchall()

        column_names = {
            column[1] for column in columns
        }

    finally:
        connection.close()

    assert "password" not in column_names
    assert "password_hash" not in column_names
    assert "score" in column_names
    assert "strength" in column_names


def test_saved_history_does_not_contain_password(history_client):
    client, _ = history_client

    response = client.post(
        "/api/history",
        json=valid_metadata()
    )

    assert "SyntheticDemo123!" not in response.get_data(as_text=True)


def test_history_record_has_timestamp(history_client):
    client, _ = history_client

    client.post("/api/history", json=valid_metadata())

    response = client.get("/api/history")

    record = response.get_json()["data"][0]

    assert "created_at" in record
    assert record["created_at"]