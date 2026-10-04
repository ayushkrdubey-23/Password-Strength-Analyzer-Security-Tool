
"""Register application API routes."""

from backend.routes.health import health_bp
from backend.routes.analyzer import analyzer_bp
from backend.routes.generator import generator_bp


def register_routes(app):
    """Register all application blueprints."""

    app.register_blueprint(health_bp)
    app.register_blueprint(analyzer_bp)
    app.register_blueprint(generator_bp)