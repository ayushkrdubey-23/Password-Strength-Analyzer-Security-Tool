"""Tests for frontend pages and static assets."""

from backend import create_app


def create_test_client():
    app = create_app()
    app.config["TESTING"] = True

    return app.test_client()


def test_homepage_loads():
    client = create_test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Password Strength Analyzer" in response.data


def test_homepage_contains_analyzer_form():
    client = create_test_client()

    response = client.get("/")

    assert b"analyzerForm" in response.data
    assert b"analysisPassword" in response.data


def test_homepage_contains_generator_form():
    client = create_test_client()

    response = client.get("/")

    assert b"generatorForm" in response.data
    assert b"passwordLength" in response.data


def test_homepage_contains_score_visualization():
    client = create_test_client()

    response = client.get("/")

    assert b"scoreChart" in response.data
    assert b"chart.umd.min.js" in response.data
    assert b"scoreValue" in response.data


def test_homepage_contains_security_metrics():
    client = create_test_client()

    response = client.get("/")

    assert b"metricLength" in response.data
    assert b"metricCharacters" in response.data
    assert b"metricRisks" in response.data


def test_homepage_contains_privacy_warning():
    client = create_test_client()

    response = client.get("/")

    assert b"synthetic demo passwords only" in response.data
    assert b"Never enter a real" in response.data
    assert b"account password" in response.data


def test_css_file_is_served():
    client = create_test_client()

    response = client.get("/css/style.css")

    assert response.status_code == 200
    assert b"font-family" in response.data
    assert b"metrics-grid" in response.data
    assert b"chart-wrapper" in response.data


def test_javascript_file_is_served():
    client = create_test_client()

    response = client.get("/js/app.js")

    assert response.status_code == 200
    assert b"/api/analyze" in response.data
    assert b"/api/generate" in response.data
    assert b"updateScoreChart" in response.data
    assert b"countDetectedRisks" in response.data