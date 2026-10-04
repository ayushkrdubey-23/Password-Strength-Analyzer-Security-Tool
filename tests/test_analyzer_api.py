
import pytest

from backend import create_app


@pytest.fixture
def client():
    """Create a Flask test client."""

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_analyzer_api_accepts_valid_password(client):
    response = client.post(
        "/api/analyze",
        json={"password": "MyUnique!Pass938"}
    )

    assert response.status_code == 200
    assert response.json["success"] is True


def test_analyzer_api_returns_analysis_data(client):
    response = client.post(
        "/api/analyze",
        json={"password": "MyUnique!Pass938"}
    )

    data = response.json["data"]

    assert "score" in data
    assert "strength" in data
    assert "analyses" in data
    assert "findings" in data
    assert "suggestions" in data


def test_analyzer_api_flags_common_password(client):
    response = client.post(
        "/api/analyze",
        json={"password": "password123"}
    )

    assert response.status_code == 200
    assert (
        response.json["data"]["analyses"]["common_password"]["detected"]
        is True
    )


def test_analyzer_api_does_not_return_password(client):
    password = "MyPrivate!Demo938"

    response = client.post(
        "/api/analyze",
        json={"password": password}
    )

    assert response.status_code == 200
    assert password not in response.get_data(as_text=True)


def test_analyzer_api_rejects_missing_password(client):
    response = client.post(
        "/api/analyze",
        json={"username": "demo"}
    )

    assert response.status_code == 400
    assert response.json["success"] is False


def test_analyzer_api_rejects_non_string_password(client):
    response = client.post(
        "/api/analyze",
        json={"password": 123456}
    )

    assert response.status_code == 400
    assert response.json["success"] is False


def test_analyzer_api_rejects_null_password(client):
    response = client.post(
        "/api/analyze",
        json={"password": None}
    )

    assert response.status_code == 400


def test_analyzer_api_rejects_invalid_json_object(client):
    response = client.post(
        "/api/analyze",
        data='["not", "an", "object"]',
        content_type="application/json"
    )

    assert response.status_code == 400


def test_analyzer_api_rejects_non_json_request(client):
    response = client.post(
        "/api/analyze",
        data="password=demo123",
        content_type="application/x-www-form-urlencoded"
    )

    assert response.status_code == 415


def test_analyzer_api_accepts_empty_string(client):
    response = client.post(
        "/api/analyze",
        json={"password": ""}
    )

    assert response.status_code == 200
    assert response.json["data"]["score"] == 0


def test_analyzer_api_rejects_get_request(client):
    response = client.get("/api/analyze")

    assert response.status_code == 405
    