"""
Password analysis history API.

History is saved only through an explicit POST request.

Only approved, non-sensitive metadata is accepted.
"""

from flask import Blueprint, jsonify, request

from backend.extensions import limiter

from backend.services.history_service import (
    save_analysis_metadata,
    get_analysis_history,
    clear_analysis_history
)


history_bp = Blueprint("history", __name__)


ALLOWED_STRENGTHS = {
    "VERY WEAK",
    "WEAK",
    "MODERATE",
    "STRONG",
    "VERY STRONG"
}


def _get_expected_strength(score):
    """Return the strength category corresponding to a score."""

    if score < 20:
        return "VERY WEAK"
    elif score < 40:
        return "WEAK"
    elif score < 60:
        return "MODERATE"
    elif score < 80:
        return "STRONG"

    return "VERY STRONG"


@history_bp.route("/api/history", methods=["POST"])
@limiter.limit("10 per minute")
def save_history():
    """
    Explicitly save non-sensitive analysis metadata.

    Passwords and hashes are not accepted.
    """

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

    required_fields = {
        "score",
        "strength",
        "findings_count",
        "character_types_count",
        "analysis_completed"
    }

    # Reject unknown fields, including passwords and hashes.
    if set(payload.keys()) != required_fields:
        return jsonify({
            "success": False,
            "error": "Request must contain only the approved history fields."
        }), 400

    score = payload["score"]
    strength = payload["strength"]
    findings_count = payload["findings_count"]
    character_types_count = payload["character_types_count"]
    analysis_completed = payload["analysis_completed"]

    if type(score) is not int or not 0 <= score <= 100:
        return jsonify({
            "success": False,
            "error": "Score must be an integer between 0 and 100."
        }), 400

    if (
        not isinstance(strength, str)
        or strength not in ALLOWED_STRENGTHS
        or strength != _get_expected_strength(score)
    ):
        return jsonify({
            "success": False,
            "error": "Strength category does not match the score."
        }), 400

    if (
        type(findings_count) is not int
        or not 0 <= findings_count <= 100
    ):
        return jsonify({
            "success": False,
            "error": "Findings count must be between 0 and 100."
        }), 400

    if (
        type(character_types_count) is not int
        or not 0 <= character_types_count <= 4
    ):
        return jsonify({
            "success": False,
            "error": "Character types count must be between 0 and 4."
        }), 400

    if type(analysis_completed) is not bool:
        return jsonify({
            "success": False,
            "error": "Analysis completed must be a boolean."
        }), 400

    metadata = {
        "score": score,
        "strength": strength,
        "findings_count": findings_count,
        "character_types_count": character_types_count,
        "analysis_completed": analysis_completed
    }

    try:
        saved_record = save_analysis_metadata(metadata)

        return jsonify({
            "success": True,
            "message": "Analysis metadata saved successfully.",
            "data": saved_record
        }), 201

    except Exception:
        return jsonify({
            "success": False,
            "error": "Analysis history could not be saved."
        }), 500


@history_bp.route("/api/history", methods=["GET"])
@limiter.limit("30 per minute")
def read_history():
    """Retrieve the latest saved analysis metadata."""

    try:
        records = get_analysis_history()

        return jsonify({
            "success": True,
            "total_records": len(records),
            "data": records
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "error": "Analysis history could not be retrieved."
        }), 500


@history_bp.route("/api/history", methods=["DELETE"])
@limiter.limit("5 per minute")
def delete_history():
    """Clear all saved analysis metadata."""

    try:
        deleted_count = clear_analysis_history()

        return jsonify({
            "success": True,
            "message": "Analysis history cleared successfully.",
            "deleted_records": deleted_count
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "error": "Analysis history could not be cleared."
        }), 500
    