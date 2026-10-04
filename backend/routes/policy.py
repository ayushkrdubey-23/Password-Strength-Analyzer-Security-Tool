"""REST API endpoint for password policy checking."""

from flask import Blueprint, jsonify, request

from backend.extensions import limiter
from backend.services.password_policy_checker import (
    check_password_policy,
)


policy_bp = Blueprint("policy", __name__)


@policy_bp.route("/api/policy/check", methods=["POST"])
@limiter.limit("10 per minute")
def check_policy():
    """Evaluate a submitted password against the default policy."""

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json.",
        }), 415

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "error": "A valid JSON object is required.",
        }), 400

    if "password" not in payload:
        return jsonify({
            "success": False,
            "error": "The password field is required.",
        }), 400

    password = payload["password"]

    if not isinstance(password, str):
        return jsonify({
            "success": False,
            "error": "Password must be a string.",
        }), 400

    try:
        result = check_password_policy(password)

        return jsonify({
            "success": True,
            "data": result,
        }), 200

    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "error": "Unable to evaluate the supplied password.",
        }), 400

    except Exception:
        # Do not log exception details because they could expose
        # sensitive request-related information.
        return jsonify({
            "success": False,
            "error": "An internal error occurred.",
        }), 500
    