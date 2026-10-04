
"""
Frontend routes.

Serves the HTML, CSS and JavaScript files from the
project's frontend directory using the Flask application.
"""

from pathlib import Path

from flask import Blueprint, abort, send_from_directory


frontend_bp = Blueprint("frontend", __name__)

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


@frontend_bp.route("/")
def index():
    """Serve the frontend homepage."""

    if not (FRONTEND_DIR / "index.html").is_file():
        abort(404)

    return send_from_directory(FRONTEND_DIR, "index.html")


@frontend_bp.route("/css/<path:filename>")
def frontend_css(filename):
    """Serve frontend CSS files."""

    return send_from_directory(FRONTEND_DIR / "css", filename)


@frontend_bp.route("/js/<path:filename>")
def frontend_js(filename):
    """Serve frontend JavaScript files."""

    return send_from_directory(FRONTEND_DIR / "js", filename)