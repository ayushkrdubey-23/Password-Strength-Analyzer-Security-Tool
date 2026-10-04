
"""
Password Analysis API Route.

Accepts a password through a JSON POST request,
runs the local analysis engine, and returns the
analysis results without exposing the submitted password.
"""

from flask import Blueprint, jsonify, request

from backend.services.password_analyzer import analyze_password


analyzer_bp = Blueprint("analyzer", __name__)


@analyzer_bp.route("/api/analyze", methods=["POST"])
def analyze_password_api():
    """Analyze a submitted password and return security findings."""

    # Accept JSON requests only.
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json."
        }), 415

    # Parse JSON without exposing parsing details or submitted values.
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "error": "Request body must be a valid JSON object."
        }), 400

    if "password" not in payload:
        return jsonify({
            "success": False,
            "error": "The password field is required."
        }), 400

    password = payload["password"]

    if not isinstance(password, str):
        return jsonify({
            "success": False,
            "error": "Password must be a string."
        }), 400

    try:
        result = analyze_password(password)

        return jsonify({
            "success": True,
            "data": result
        }), 200

    except Exception:
        # Do not log or include submitted password information.
        return jsonify({
            "success": False,
            "error": "Password analysis could not be completed."
        }), 500