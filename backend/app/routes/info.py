from flask import Blueprint, jsonify, current_app, request
from app.services.metrics_tracker import tracker

info_bp = Blueprint("info", __name__)

@info_bp.route("/", methods=["GET"])
def index():
    """Application landing endpoint."""
    accept_header = request.headers.get("Accept", "")
    data = {
        "project": current_app.config.get("APP_NAME", "DevOps Self-Healing System"),
        "version": current_app.config.get("VERSION", "1.0.0"),
        "framework": "Python Flask (WSGI)",
        "server": "Gunicorn",
        "reverse_proxy": "Nginx",
        "deployment_method": "Ansible Automation",
        "monitoring": "Nagios Core with Ansible Self-Healing",
        "endpoints": {
            "landing": "/",
            "liveness": "/healthz",
            "readiness": "/readyz",
            "status": "/api/v1/status",
            "info": "/api/v1/info",
            "metrics": "/api/v1/metrics"
        }
    }
    return jsonify(data), 200

@info_bp.route("/api/v1/info", methods=["GET"])
def get_info():
    """Return safe non-sensitive application environment information."""
    return jsonify({
        "service": current_app.config.get("SERVICE_NAME", "python-backend"),
        "application": current_app.config.get("APP_NAME", "DevOps Self-Healing System"),
        "environment": current_app.config.get("ENV", "production"),
        "version": current_app.config.get("VERSION", "1.0.0"),
        "framework": "Flask 3.x",
        "deployment_mode": "Gunicorn WSGI via Nginx Reverse Proxy",
        "self_healing_enabled": True
    }), 200

@info_bp.route("/api/v1/metrics", methods=["GET"])
def get_metrics():
    """Return lightweight, safe application performance metrics."""
    return jsonify(tracker.get_metrics()), 200
