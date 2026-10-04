
import pytest

from backend import create_app


@pytest.fixture
def app():
    """
    Create a Flask application for testing.
    """

    application = create_app()

    application.config.update({
        "TESTING": True
    })

    yield application


@pytest.fixture
def client(app):
    """
    Create a test client.
    """

    return app.test_client()


def test_application_initialization(app):
    assert app is not None


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "success"
    assert "message" in data


def test_unknown_endpoint(client):
    response = client.get("/unknown-endpoint")

    assert response.status_code == 404

    data = response.get_json()

    assert data["status"] == "error"


def test_security_headers(client):
    response = client.get("/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"


def test_health_does_not_return_password(client):
    response = client.get("/health")

    data = response.get_json()

    assert "password" not in data
    