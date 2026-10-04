"""API tests for the password policy endpoint."""

from backend import create_app


def get_test_client():
    """Create a Flask test client."""

    app = create_app()
    app.config["TESTING"] = True

    return app.test_client()


def test_policy_endpoint_accepts_valid_request():
    client = get_test_client()

    response = client.post(
        "/api/policy/check",
        json={"password": "Violet!Cedar#74Moon"},
    )

    assert response.status_code == 200

    body = response.get_json()

    assert body["success"] is True
    assert body["data"]["total_checks"] == 10


def test_policy_endpoint_returns_individual_checks():
    client = get_test_client()

    response = client.post(
        "/api/policy/check",
        json={"password": "Violet!Cedar#74Moon"},
    )

    body = response.get_json()

    assert len(body["data"]["checks"]) == 10
    assert "recommendations" in body["data"]


def test_policy_endpoint_does_not_return_password():
    client = get_test_client()
    password = "Synthetic!Password987"

    response = client.post(
        "/api/policy/check",
        json={"password": password},
    )

    assert password not in response.get_data(as_text=True)


def test_policy_endpoint_rejects_missing_password():
    client = get_test_client()

    response = client.post(
        "/api/policy/check",
        json={},
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_policy_endpoint_rejects_non_string_password():
    client = get_test_client()

    response = client.post(
        "/api/policy/check",
        json={"password": 123456},
    )

    assert response.status_code == 400


def test_policy_endpoint_requires_json():
    client = get_test_client()

    response = client.post(
        "/api/policy/check",
        data="password=example",
        content_type="application/x-www-form-urlencoded",
    )

    assert response.status_code == 415