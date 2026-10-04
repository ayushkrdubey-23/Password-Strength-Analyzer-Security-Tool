
import os


def get_config():
    """
    Return application configuration.

    Environment variables are loaded before this
    function is called.
    """

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

        "MAX_CONTENT_LENGTH": 16 * 1024
    }
