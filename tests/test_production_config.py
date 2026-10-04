
import pytest

from backend.config import get_config


def test_development_configuration_uses_development_mode(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.delenv("APP_SECRET_KEY", raising=False)

    config = get_config()

    assert config["APP_ENV"] == "development"
    assert config["SECRET_KEY"] == (
        "development-only-change-this-secret"
    )


def test_production_configuration_rejects_default_secret(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv(
        "APP_SECRET_KEY",
        "development-only-change-this-secret",
    )

    with pytest.raises(RuntimeError):
        get_config()


def test_production_configuration_rejects_placeholder_secret(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv(
        "APP_SECRET_KEY",
        "replace_with_a_random_secret_before_use",
    )

    with pytest.raises(RuntimeError):
        get_config()


def test_production_configuration_accepts_custom_secret(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv(
        "APP_SECRET_KEY",
        "synthetic-test-secret-not-for-real-deployment",
    )

    config = get_config()

    assert config["APP_ENV"] == "production"
    assert config["SECRET_KEY"] == (
        "synthetic-test-secret-not-for-real-deployment"
    )
    assert config["SESSION_COOKIE_SECURE"] is True


def test_development_cookie_configuration(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.delenv("APP_SECRET_KEY", raising=False)

    config = get_config()

    assert config["SESSION_COOKIE_HTTPONLY"] is True
    assert config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert config["SESSION_COOKIE_SECURE"] is False