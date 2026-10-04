
"""Centralized application configuration."""

import os


def get_config():
    """Return application configuration."""

    app_env = os.getenv("APP_ENV", "development").strip().lower()
    secret_key = os.getenv(
        "APP_SECRET_KEY",
        "development-only-change-this-secret",
    )

    if app_env == "production":
        if (
            not secret_key
            or secret_key == "development-only-change-this-secret"
            or secret_key == "replace_with_a_random_secret_before_use"
        ):
            raise RuntimeError(
                "A strong APP_SECRET_KEY must be configured in production."
            )

    return {
        "APP_NAME": os.getenv(
            "APP_NAME",
            "Password Strength Analyzer",
        ),
        "APP_ENV": app_env,
        "APP_HOST": os.getenv(
            "APP_HOST",
            "127.0.0.1",
        ),
        "APP_PORT": int(
            os.getenv("APP_PORT", "5000"),
        ),
        "SECRET_KEY": secret_key,
        "DATABASE_PATH": os.getenv(
            "DATABASE_PATH",
            "instance/analytics.db",
        ),
        "MAX_CONTENT_LENGTH": 16 * 1024,
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "SESSION_COOKIE_SECURE": app_env == "production",
    }