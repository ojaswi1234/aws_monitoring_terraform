import os
from flask import Blueprint, jsonify, current_app, request, send_from_directory
from app.services.metrics_tracker import tracker

info_bp = Blueprint("info", __name__)

@info_bp.route("/", methods=["GET"])
def index():
    """Application landing endpoint: serves dashboard for browsers, JSON for APIs."""
    accept_header = request.headers.get("Accept", "")
    frontend_dir = os.path.abspath(os.path.join(current_app.root_path, "../../frontend"))

    # If accessed by a web browser, serve the dashboard
    if "text/html" in accept_header and "application/json" not in accept_header and os.path.exists(os.path.join(frontend_dir, "index.html")):
        return send_from_directory(frontend_dir, "index.html")

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
            "metrics": "/api/v1/metrics",
            "infrastructure": "/api/v1/infrastructure"
        }
    }
    return jsonify(data), 200

# Static asset routes for local execution without Nginx
@info_bp.route("/css/<path:filename>", methods=["GET"])
def serve_css(filename):
    frontend_dir = os.path.abspath(os.path.join(current_app.root_path, "../../frontend/css"))
    return send_from_directory(frontend_dir, filename)

@info_bp.route("/js/<path:filename>", methods=["GET"])
def serve_js(filename):
    frontend_dir = os.path.abspath(os.path.join(current_app.root_path, "../../frontend/js"))
    return send_from_directory(frontend_dir, filename)

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

@info_bp.route("/api/v1/infrastructure", methods=["GET"])
def get_infrastructure():
    """Return provisioned AWS cloud topology & instance details."""
    return jsonify({
        "cloud_provider": "Amazon Web Services (AWS)",
        "region": "us-east-1",
        "vpc_cidr": "10.0.0.0/16",
        "subnet_cidr": "10.0.1.0/24",
        "instances": [
            {
                "id": "i-091a4b872c019d3f1",
                "name": "monitor-server",
                "role": "Nagios Core 4.x & Ansible Engine",
                "type": "t2.micro",
                "private_ip": "10.0.1.50",
                "public_ip": "54.210.42.118",
                "security_group": "devops-self-healing-monitor-sg",
                "services": ["nagios4", "apache2"],
                "status": "running"
            },
            {
                "id": "i-0b5c9e217d832e4a2",
                "name": "app-server",
                "role": "Nginx Reverse Proxy + Gunicorn + Flask",
                "type": "t2.micro",
                "private_ip": "10.0.1.60",
                "public_ip": "54.210.42.119",
                "security_group": "devops-self-healing-app-sg",
                "services": ["nginx", "flask-backend", "nagios-nrpe-server"],
                "status": "running"
            }
        ]
    }), 200
