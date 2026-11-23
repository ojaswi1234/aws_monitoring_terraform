from flask import Blueprint, jsonify, current_app
from app.services.metrics_tracker import tracker

status_bp = Blueprint("status", __name__, url_prefix="/api/v1")

@status_bp.route("/status", methods=["GET"])
def get_status():
    """Return application operational status."""
    return jsonify({
        "application": current_app.config.get("APP_NAME", "DevOps Self-Healing System"),
        "status": "running",
        "backend": "Flask",
        "version": current_app.config.get("VERSION", "1.0.0"),
        "uptime_seconds": tracker.get_uptime_seconds()
    }), 200
