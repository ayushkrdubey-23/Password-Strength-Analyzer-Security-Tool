
"""
Secure Password Generator API.

Generates passwords using the Python secrets module.
Generated passwords are returned to the caller but
are never stored or logged by this endpoint.
"""

from flask import Blueprint, jsonify, request

from backend.services.password_generator import generate_password


generator_bp = Blueprint("generator", __name__)


@generator_bp.route("/api/generate", methods=["POST"])
def generate_password_api():
    """Generate a secure password using the supplied options."""

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json."
        }), 415

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "error": "Request body must be a valid JSON object."
        }), 400

    try:
        password = generate_password(
            length=payload.get("length", 20),
            include_lowercase=payload.get("include_lowercase", True),
            include_uppercase=payload.get("include_uppercase", True),
            include_digits=payload.get("include_digits", True),
            include_symbols=payload.get("include_symbols", True)
        )

        return jsonify({
            "success": True,
            "data": {
                "password": password,
                "length": len(password),
                "message": "Secure password generated successfully."
            }
        }), 200

    except (TypeError, ValueError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400