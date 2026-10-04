
from flask import Flask, jsonify
from dotenv import load_dotenv

from backend.config import get_config
from backend.routes import register_routes


def create_app():
    """
    Create and configure the Flask application.
    """

    # Load environment configuration.
    load_dotenv()

    app = Flask(__name__)

    # Apply centralized configuration.
    app.config.update(get_config())

    # Register API routes.
    register_routes(app)

    @app.after_request
    def add_security_headers(response):
        """
        Add basic security-related HTTP headers.
        """

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"

        return response

    @app.errorhandler(404)
    def not_found(error):
        """
        Return a generic JSON 404 response.
        """

        return jsonify({
            "status": "error",
            "message": "The requested endpoint was not found."
        }), 404

    @app.errorhandler(413)
    def request_too_large(error):
        """
        Reject requests that exceed the configured size.
        """

        return jsonify({
            "status": "error",
            "message": "Request payload exceeds the allowed size."
        }), 413

    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Return a generic internal error response.

        Never include submitted request data in errors.
        """

        return jsonify({
            "status": "error",
            "message": "An internal server error occurred."
        }), 500

    return app
