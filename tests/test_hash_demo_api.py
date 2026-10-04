
"""API tests for the educational Argon2id demonstration."""

import pytest

from backend import create_app


@pytest.fixture
def client():
    """Create an isolated Flask test client."""

    app = create_app()

    app.config.update({
        "TESTING": True,
        "RATELIMIT_ENABLED": False
    })

    with app.test_client() as test_client:
        yield test_client


def test_hash_endpoint_returns_argon2id_hash(client):
    response = client.post(
        "/api/hash-demo/hash",
        json={"password": "Demo-Password-2026!"}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["algorithm"] == "Argon2id"
    assert data["encoded_hash"].startswith("$argon2id$")
    assert data["stored"] is False


def test_hash_endpoint_does_not_return_plaintext_password(client):
    password = "Demo-Password-2026!"

    response = client.post(
        "/api/hash-demo/hash",
        json={"password": password}
    )

    assert response.status_code == 200
    assert password not in response.get_data(as_text=True)


def test_hash_endpoint_rejects_empty_password(client):
    response = client.post(
        "/api/hash-demo/hash",
        json={"password": ""}
    )

    assert response.status_code == 400


def test_hash_endpoint_rejects_missing_password(client):
    response = client.post(
        "/api/hash-demo/hash",
        json={}
    )

    assert response.status_code == 400


def test_hash_endpoint_rejects_extra_fields(client):
    response = client.post(
        "/api/hash-demo/hash",
        json={
            "password": "Demo-Password-2026!",
            "extra": "unexpected"
        }
    )

    assert response.status_code == 400


def test_hash_endpoint_requires_json(client):
    response = client.post(
        "/api/hash-demo/hash",
        data="password=Demo-Password"
    )

    assert response.status_code == 415


def test_verify_endpoint_accepts_correct_password(client):
    password = "Demo-Password-2026!"

    hash_response = client.post(
        "/api/hash-demo/hash",
        json={"password": password}
    )

    encoded_hash = hash_response.get_json()["encoded_hash"]

    response = client.post(
        "/api/hash-demo/verify",
        json={
            "password": password,
            "encoded_hash": encoded_hash
        }
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["matches"] is True
    assert data["algorithm"] == "Argon2id"


def test_verify_endpoint_rejects_incorrect_password(client):
    hash_response = client.post(
        "/api/hash-demo/hash",
        json={"password": "Correct-Password-2026!"}
    )

    encoded_hash = hash_response.get_json()["encoded_hash"]

    response = client.post(
        "/api/hash-demo/verify",
        json={
            "password": "Incorrect-Password-2026!",
            "encoded_hash": encoded_hash
        }
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["matches"] is False


def test_verify_endpoint_rejects_malformed_hash(client):
    response = client.post(
        "/api/hash-demo/verify",
        json={
            "password": "Demo-Password-2026!",
            "encoded_hash": "invalid-hash"
        }
    )

    assert response.status_code == 400


def test_verify_endpoint_rejects_missing_fields(client):
    response = client.post(
        "/api/hash-demo/verify",
        json={"password": "Demo-Password-2026!"}
    )

    assert response.status_code == 400


def test_verify_endpoint_rejects_extra_fields(client):
    response = client.post(
        "/api/hash-demo/verify",
        json={
            "password": "Demo-Password-2026!",
            "encoded_hash": "invalid-hash",
            "extra": "unexpected"
        }
    )

    assert response.status_code == 400


def test_verify_endpoint_requires_json(client):
    response = client.post(
        "/api/hash-demo/verify",
        data="password=Demo-Password"
    )

    assert response.status_code == 415


def test_hash_response_does_not_expose_password(client):
    password = "Sensitive-Demo-Password-2026!"

    response = client.post(
        "/api/hash-demo/hash",
        json={"password": password}
    )

    response_text = response.get_data(as_text=True)

    assert password not in response_text
    assert "encoded_hash" in response_text


def test_hash_demo_does_not_save_password_or_hash_to_history(client):
    password = "Demo-Password-2026!"

    hash_response = client.post(
        "/api/hash-demo/hash",
        json={"password": password}
    )

    assert hash_response.status_code == 200

    encoded_hash = hash_response.get_json()["encoded_hash"]

    history_response = client.get("/api/history")

    assert history_response.status_code == 200

    history_text = history_response.get_data(as_text=True)

    assert password not in history_text
    assert encoded_hash not in history_text