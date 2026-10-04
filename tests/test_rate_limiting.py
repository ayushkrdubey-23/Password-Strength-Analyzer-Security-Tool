"""Tests for API rate limiting and abuse protection."""

from backend import create_app


def test_analyzer_endpoint_is_limited_after_ten_requests():
    """The eleventh analysis request should receive HTTP 429."""

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    test_ip = "198.51.100.21"

    for _ in range(10):
        response = client.post(
            "/api/analyze",
            json={"password": "Demo!SecurePassword2026"},
            environ_overrides={"REMOTE_ADDR": test_ip}
        )
        assert response.status_code == 200

    response = client.post(
        "/api/analyze",
        json={"password": "Another!DemoPassword2026"},
        environ_overrides={"REMOTE_ADDR": test_ip}
    )

    assert response.status_code == 429
    assert response.get_json()["success"] is False
    assert "Too many requests" in response.get_json()["error"]


def test_generator_endpoint_is_limited_after_ten_requests():
    """The eleventh generation request should receive HTTP 429."""

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    test_ip = "198.51.100.22"

    for _ in range(10):
        response = client.post(
            "/api/generate",
            json={"length": 20},
            environ_overrides={"REMOTE_ADDR": test_ip}
        )
        assert response.status_code == 200

    response = client.post(
        "/api/generate",
        json={"length": 20},
        environ_overrides={"REMOTE_ADDR": test_ip}
    )

    assert response.status_code == 429
    assert response.get_json()["success"] is False
    assert "Too many requests" in response.get_json()["error"]


def test_health_endpoint_is_not_rate_limited():
    """The health endpoint should remain available beyond ten requests."""

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    test_ip = "198.51.100.23"

    for _ in range(12):
        response = client.get(
            "/health",
            environ_overrides={"REMOTE_ADDR": test_ip}
        )

        assert response.status_code == 200