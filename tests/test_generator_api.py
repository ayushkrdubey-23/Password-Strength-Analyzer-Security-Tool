
import string

import pytest

from backend import create_app


@pytest.fixture
def client():
    """Create a Flask test client."""

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_generator_api_generates_password(client):
    response = client.post(
        "/api/generate",
        json={}
    )

    assert response.status_code == 200
    assert response.json["success"] is True
    assert "password" in response.json["data"]


def test_generator_api_uses_default_length(client):
    response = client.post(
        "/api/generate",
        json={}
    )

    assert response.json["data"]["length"] == 20


def test_generator_api_accepts_custom_length(client):
    response = client.post(
        "/api/generate",
        json={"length": 32}
    )

    assert response.status_code == 200
    assert response.json["data"]["length"] == 32
    assert len(response.json["data"]["password"]) == 32


def test_generator_api_includes_all_default_categories(client):
    response = client.post(
        "/api/generate",
        json={}
    )

    password = response.json["data"]["password"]

    assert any(char in string.ascii_lowercase for char in password)
    assert any(char in string.ascii_uppercase for char in password)
    assert any(char in string.digits for char in password)
    assert any(
        char in "!@#$%^&*()-_=+[]{};:,.?"
        for char in password
    )


def test_generator_api_supports_selected_categories(client):
    response = client.post(
        "/api/generate",
        json={
            "length": 16,
            "include_lowercase": True,
            "include_uppercase": False,
            "include_digits": True,
            "include_symbols": False
        }
    )

    assert response.status_code == 200

    password = response.json["data"]["password"]

    assert len(password) == 16
    assert any(char in string.ascii_lowercase for char in password)
    assert any(char in string.digits for char in password)
    assert all(char in string.ascii_lowercase + string.digits for char in password)


def test_generator_api_rejects_short_length(client):
    response = client.post(
        "/api/generate",
        json={"length": 5}
    )

    assert response.status_code == 400
    assert response.json["success"] is False


def test_generator_api_rejects_excessive_length(client):
    response = client.post(
        "/api/generate",
        json={"length": 200}
    )

    assert response.status_code == 400


def test_generator_api_rejects_string_length(client):
    response = client.post(
        "/api/generate",
        json={"length": "20"}
    )

    assert response.status_code == 400


def test_generator_api_rejects_when_no_category_is_selected(client):
    response = client.post(
        "/api/generate",
        json={
            "include_lowercase": False,
            "include_uppercase": False,
            "include_digits": False,
            "include_symbols": False
        }
    )

    assert response.status_code == 400


def test_generator_api_rejects_non_boolean_category(client):
    response = client.post(
        "/api/generate",
        json={"include_digits": 1}
    )

    assert response.status_code == 400


def test_generator_api_rejects_non_json_request(client):
    response = client.post(
        "/api/generate",
        data="length=20",
        content_type="application/x-www-form-urlencoded"
    )

    assert response.status_code == 415


def test_generator_api_rejects_invalid_json_object(client):
    response = client.post(
        "/api/generate",
        data='["invalid", "body"]',
        content_type="application/json"
    )

    assert response.status_code == 400


def test_generator_api_rejects_get_request(client):
    response = client.get("/api/generate")

    assert response.status_code == 405
    