
import pytest

from backend import create_app


@pytest.fixture
def app():
    """Create a Flask application for testing."""

    application = create_app()

    application.config.update({
        "TESTING": True,
        "RATELIMIT_ENABLED": False,
    })

    yield application


@pytest.fixture
def client(app):
    """Create a test client."""

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


def test_content_security_policy(client):
    response = client.get("/")

    policy = response.headers["Content-Security-Policy"]

    assert "default-src 'self'" in policy
    assert "object-src 'none'" in policy
    assert "frame-ancestors 'none'" in policy
    assert "https://cdn.jsdelivr.net" in policy
    assert "https://unpkg.com" in policy


def test_additional_security_headers(client):
    response = client.get("/health")

    assert response.headers["Permissions-Policy"] == (
        "camera=(), microphone=(), geolocation=()"
    )

    assert response.headers["Cross-Origin-Resource-Policy"] == "same-origin"


def test_api_responses_disable_caching(client):
    response = client.get("/health")

    assert response.headers["Cache-Control"] == "no-store"


def test_http_response_does_not_enable_hsts(client):
    response = client.get("/health")

    assert "Strict-Transport-Security" not in response.headers


def test_health_does_not_return_password(client):
    response = client.get("/health")

    data = response.get_json()

    assert "password" not in data