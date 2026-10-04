
from backend.routes.health import health_bp


def register_routes(app):
    """
    Register application routes.
    """

    app.register_blueprint(health_bp)
    