"""Register application routes."""

from backend.routes.health import health_bp
from backend.routes.analyzer import analyzer_bp
from backend.routes.generator import generator_bp
from backend.routes.frontend import frontend_bp
from backend.routes.policy import policy_bp
from backend.routes.docs import docs_bp


def register_routes(app):
    """Register all application blueprints."""

    app.register_blueprint(health_bp)
    app.register_blueprint(analyzer_bp)
    app.register_blueprint(generator_bp)
    app.register_blueprint(policy_bp)
    app.register_blueprint(docs_bp)
    app.register_blueprint(frontend_bp)