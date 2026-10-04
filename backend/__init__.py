
from flask import Flask, jsonify, request
from dotenv import load_dotenv

from backend.config import get_config
from backend.extensions import limiter
from backend.routes import register_routes


def create_app():
    """Create and configure the Flask application."""

    load_dotenv()

    app = Flask(__name__)

    # Apply centralized configuration.
    app.config.update(get_config())

    # Enable standard rate-limit response headers.
    app.config["RATELIMIT_HEADERS_ENABLED"] = True
    app.config["RATELIMIT_SWALLOW_ERRORS"] = False

    # Initialize rate limiting before registering routes.
    limiter.init_app(app)

    # Register API and frontend routes.
    register_routes(app)

    @app.after_request
    def add_security_headers(response):
        """Add security-related HTTP response headers."""

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"

        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://unpkg.com; "
            "font-src 'self' https://unpkg.com data:; "
            "img-src 'self' data:; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'none'"
        )

        # Enable HSTS only for secure HTTPS requests.
        if request.is_secure:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000"
            )

        # Prevent caching of API and health-check responses.
        if request.path.startswith("/api/") or request.path == "/health":
            response.headers["Cache-Control"] = "no-store"

        return response

    @app.errorhandler(404)
    def not_found(error):
        """Return a generic JSON 404 response."""

        return jsonify({
            "status": "error",
            "message": "The requested endpoint was not found.",
        }), 404

    @app.errorhandler(413)
    def request_too_large(error):
        """Reject requests that exceed the configured size."""

        return jsonify({
            "status": "error",
            "message": "Request payload exceeds the allowed size.",
        }), 413

    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Return a generic response when a client exceeds its limit."""

        return jsonify({
            "success": False,
            "error": "Too many requests. Please wait before trying again.",
        }), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        """Return a generic internal error response."""

        return jsonify({
            "status": "error",
            "message": "An internal server error occurred.",
        }), 500

    return app