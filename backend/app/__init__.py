from flask import Flask, jsonify
from app.config import get_config
from app.services.metrics_tracker import tracker

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # Global request counter for safe metrics
    @app.before_request
    def before_request_hook():
        tracker.record_request()

    # Register blueprints
    from app.routes.health import health_bp
    from app.routes.status import status_bp
    from app.routes.info import info_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(info_bp)

    # Standardized error handlers
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found on this server."
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({
            "error": "Method Not Allowed",
            "message": "The method is not allowed for the requested URL."
        }), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred."
        }), 500

    return app
