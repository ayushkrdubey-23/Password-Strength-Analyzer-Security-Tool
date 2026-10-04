"""Centralized application configuration."""

import os


def get_config():
    """Return application configuration."""

    return {
        "APP_NAME": os.getenv(
            "APP_NAME",
            "Password Strength Analyzer"
        ),

        "APP_ENV": os.getenv(
            "APP_ENV",
            "development"
        ),

        "APP_HOST": os.getenv(
            "APP_HOST",
            "127.0.0.1"
        ),

        "APP_PORT": int(
            os.getenv("APP_PORT", "5000")
        ),

        "SECRET_KEY": os.getenv(
            "APP_SECRET_KEY",
            "development-only-change-this-secret"
        ),

        "DATABASE_PATH": os.getenv(
            "DATABASE_PATH",
            "instance/analytics.db"
        ),

        "MAX_CONTENT_LENGTH": 16 * 1024
    }