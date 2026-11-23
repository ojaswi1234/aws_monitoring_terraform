import os
import json
from flask import Blueprint, jsonify, current_app, request, send_from_directory
from app.services.metrics_tracker import tracker

info_bp = Blueprint("info", __name__)

def load_aws_infrastructure():
    """Dynamically load real AWS infrastructure topology from Terraform state if available."""
    candidates = [
        os.path.abspath(os.path.join(current_app.root_path, "../../terraform/terraform.tfstate")),
        "/home/ob/devops-self-healing-project/terraform/terraform.tfstate",
        os.path.join(os.getcwd(), "terraform/terraform.tfstate")
    ]
    
    tfstate_path = None
    for c in candidates:
        if os.path.exists(c):
            tfstate_path = c
            break

    if tfstate_path:
        try:
            with open(tfstate_path, "r") as f:
                state = json.load(f)
            
            instances = []
            vpc_id = "vpc-0406f052d9dbad5a3"
            subnet_id = "subnet-01ba87b9561b419e6"

            for res in state.get("resources", []):
                res_type = res.get("type")
                if res_type == "aws_vpc":
                    for inst in res.get("instances", []):
                        vpc_id = inst.get("attributes", {}).get("id", vpc_id)
                elif res_type == "aws_subnet":
                    for inst in res.get("instances", []):
                        subnet_id = inst.get("attributes", {}).get("id", subnet_id)
                elif res_type == "aws_instance":
                    res_name = res.get("name")
                    for inst in res.get("instances", []):
                        attrs = inst.get("attributes", {})
                        is_monitor = "monitor" in res_name
                        instances.append({
                            "id": attrs.get("id"),
                            "name": attrs.get("tags", {}).get("Name", res_name),
                            "role": "Nagios Core 4.x & Ansible Engine" if is_monitor else "Nginx + Gunicorn + Flask REST API",
                            "type": attrs.get("instance_type", "t2.micro"),
                            "private_ip": attrs.get("private_ip"),
                            "public_ip": attrs.get("public_ip"),
                            "security_group": attrs.get("vpc_security_group_ids", ["sg-default"])[0] if attrs.get("vpc_security_group_ids") else "sg-default",
                            "services": ["nagios4", "apache2"] if is_monitor else ["nginx", "flask-backend", "nagios-nrpe-server"],
                            "status": attrs.get("instance_state", "running")
                        })
            if instances:
                instances.sort(key=lambda x: 0 if "monitor" in x["name"] else 1)
                return {
                    "cloud_provider": "Amazon Web Services (AWS)",
                    "region": "us-east-1",
                    "vpc_id": vpc_id,
                    "vpc_cidr": "10.0.0.0/16",
                    "subnet_id": subnet_id,
                    "subnet_cidr": "10.0.1.0/24",
                    "instances": instances
                }
        except Exception:
            pass

    # Exact live AWS provisioned values fallback
    return {
        "cloud_provider": "Amazon Web Services (AWS)",
        "region": "us-east-1",
        "vpc_id": "vpc-0406f052d9dbad5a3",
        "vpc_cidr": "10.0.0.0/16",
        "subnet_id": "subnet-01ba87b9561b419e6",
        "subnet_cidr": "10.0.1.0/24",
        "instances": [
            {
                "id": "i-0839b0eeb087d3e45",
                "name": "devops-self-healing-monitor-server",
                "role": "Nagios Core 4.x & Ansible Engine",
                "type": "t2.micro",
                "private_ip": "10.0.1.28",
                "public_ip": "44.223.101.208",
                "security_group": "sg-0db558370655a1ea2",
                "services": ["nagios4", "apache2"],
                "status": "running"
            },
            {
                "id": "i-00f3e3f270983d9a5",
                "name": "devops-self-healing-app-server",
                "role": "Nginx Reverse Proxy + Gunicorn + Flask",
                "type": "t2.micro",
                "private_ip": "10.0.1.45",
                "public_ip": "98.84.41.102",
                "security_group": "sg-0f351010186238c49",
                "services": ["nginx", "flask-backend", "nagios-nrpe-server"],
                "status": "running"
            }
        ]
    }

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
    return jsonify(load_aws_infrastructure()), 200
