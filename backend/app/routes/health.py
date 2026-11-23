import os
from flask import Blueprint, jsonify, current_app

health_bp = Blueprint("health", __name__)

CRASH_FLAG_FILE = "/tmp/devops_simulated_crash"

@health_bp.route("/healthz", methods=["GET"])
def health_check():
    """Liveness check confirming the Flask application process is alive."""
    if os.path.exists(CRASH_FLAG_FILE):
        return jsonify({
            "status": "CRITICAL",
            "service": current_app.config.get("SERVICE_NAME", "python-backend"),
            "error": "Service Failure: Gunicorn process terminated (Simulated Crash)",
            "nagios_state": "CRITICAL"
        }), 503

    return jsonify({
        "status": "ok",
        "service": current_app.config.get("SERVICE_NAME", "python-backend"),
        "nagios_state": "OK"
    }), 200

@health_bp.route("/readyz", methods=["GET"])
def readiness_check():
    """Readiness check confirming backend is prepared to serve incoming traffic."""
    if os.path.exists(CRASH_FLAG_FILE):
        return jsonify({
            "status": "UNREADY",
            "service": "python-backend",
            "ready": False,
            "reason": "Backend dependency offline"
        }), 503

    is_ready = bool(current_app.config.get("SERVICE_NAME"))
    if not is_ready:
        return jsonify({
            "status": "unhealthy",
            "service": "python-backend",
            "ready": False,
            "reason": "Configuration missing"
        }), 503

    return jsonify({
        "status": "ready",
        "service": current_app.config.get("SERVICE_NAME", "python-backend"),
        "ready": True
    }), 200

# Interactive simulation endpoints for live demonstration
@health_bp.route("/api/v1/simulate/crash", methods=["POST", "GET"])
def simulate_crash():
    with open(CRASH_FLAG_FILE, "w") as f:
        f.write("CRASHED")
    return jsonify({
        "action": "simulate_crash",
        "status": "CRITICAL",
        "message": "Simulated backend failure activated! /healthz now returning 503 CRITICAL.",
        "simulated": True
    }), 200

@health_bp.route("/api/v1/simulate/recover", methods=["POST", "GET"])
def simulate_recover():
    if os.path.exists(CRASH_FLAG_FILE):
        os.remove(CRASH_FLAG_FILE)
    return jsonify({
        "action": "simulate_recover",
        "status": "OK",
        "message": "Ansible recovery executed! Service restored to healthy 200 OK state.",
        "simulated": False
    }), 200
