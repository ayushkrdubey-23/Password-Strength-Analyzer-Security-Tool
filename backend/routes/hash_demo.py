"""Educational Argon2id hashing demonstration API."""

from flask import Blueprint, jsonify, request

from backend.extensions import limiter
from backend.services.argon2_demo import (
    hash_password_for_demo,
    verify_password_for_demo,
)


hash_demo_bp = Blueprint("hash_demo", __name__)


@hash_demo_bp.route("/api/hash-demo/hash", methods=["POST"])
@limiter.limit("10 per minute")
def create_demo_hash():
    """Generate an Argon2id hash for educational demonstration."""

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json."
        }), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "A valid JSON object is required."
        }), 400

    if set(data.keys()) != {"password"}:
        return jsonify({
            "success": False,
            "error": "Provide only the password field."
        }), 400

    password = data.get("password")

    if not isinstance(password, str):
        return jsonify({
            "success": False,
            "error": "Password must be a string."
        }), 400

    if not password:
        return jsonify({
            "success": False,
            "error": "Password cannot be empty."
        }), 400

    if len(password) > 1024:
        return jsonify({
            "success": False,
            "error": "Password exceeds the maximum allowed length."
        }), 400

    try:
        encoded_hash = hash_password_for_demo(password)

        return jsonify({
            "success": True,
            "algorithm": "Argon2id",
            "encoded_hash": encoded_hash,
            "stored": False,
            "message": (
                "Educational demonstration only. "
                "The password and generated hash were not saved."
            )
        }), 200

    except (TypeError, ValueError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception:
        return jsonify({
            "success": False,
            "error": "Hash generation failed."
        }), 500


@hash_demo_bp.route("/api/hash-demo/verify", methods=["POST"])
@limiter.limit("10 per minute")
def verify_demo_hash():
    """Verify a password against an Argon2id encoded hash."""

    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Content-Type must be application/json."
        }), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "A valid JSON object is required."
        }), 400

    if set(data.keys()) != {"password", "encoded_hash"}:
        return jsonify({
            "success": False,
            "error": "Provide password and encoded_hash fields only."
        }), 400

    password = data.get("password")
    encoded_hash = data.get("encoded_hash")

    if not isinstance(password, str) or not isinstance(encoded_hash, str):
        return jsonify({
            "success": False,
            "error": "Password and encoded_hash must be strings."
        }), 400

    if not password or not encoded_hash:
        return jsonify({
            "success": False,
            "error": "Password and encoded_hash cannot be empty."
        }), 400

    if len(password) > 1024 or len(encoded_hash) > 512:
        return jsonify({
            "success": False,
            "error": "One or more fields exceed the allowed length."
        }), 400

    try:
        matches = verify_password_for_demo(password, encoded_hash)

        return jsonify({
            "success": True,
            "matches": matches,
            "algorithm": "Argon2id",
            "stored": False,
            "message": (
                "Password verification completed. "
                "No password or hash was saved."
            )
        }), 200

    except (TypeError, ValueError) as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception:
        return jsonify({
            "success": False,
            "error": "Password verification failed."
        }), 500