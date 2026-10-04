"""Tests for Swagger UI and OpenAPI documentation routes."""

from backend import create_app


def get_test_client():
    """Create a Flask test client."""

    app = create_app()
    app.config["TESTING"] = True

    return app.test_client()


def test_swagger_ui_route_returns_success():
    client = get_test_client()

    response = client.get("/apidocs")

    assert response.status_code == 200
    assert b"swagger-ui" in response.data.lower()


def test_swagger_ui_references_openapi_specification():
    client = get_test_client()

    response = client.get("/apidocs")

    assert response.status_code == 200
    assert b"/openapi.json" in response.data


def test_openapi_json_route_returns_success():
    client = get_test_client()

    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.is_json


def test_openapi_document_has_expected_version():
    client = get_test_client()

    response = client.get("/openapi.json")
    specification = response.get_json()

    assert specification["openapi"] == "3.0.3"


def test_openapi_document_lists_all_api_endpoints():
    client = get_test_client()

    specification = client.get("/openapi.json").get_json()

    paths = specification["paths"]

    assert "/health" in paths
    assert "/api/analyze" in paths
    assert "/api/generate" in paths
    assert "/api/policy/check" in paths


def test_openapi_specification_does_not_include_real_password():
    client = get_test_client()

    response = client.get("/openapi.json")

    assert b"Violet!Cedar#74Moon" in response.data
    assert b"my-real-password" not in response.data


def test_openapi_response_disables_caching():
    client = get_test_client()

    response = client.get("/openapi.json")

    assert response.headers["Cache-Control"] == "no-store"
    