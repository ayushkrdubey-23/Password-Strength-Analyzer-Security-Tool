
from flask import Blueprint, current_app, jsonify


health_bp = Blueprint(
    "health",
    __name__
)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Return application health information.

    This endpoint does not accept or process passwords.
    """

    return jsonify({
        "status": "success",
        "message": "Application is running successfully.",
        "application": current_app.config["APP_NAME"],
        "environment": current_app.config["APP_ENV"]
    }), 200
