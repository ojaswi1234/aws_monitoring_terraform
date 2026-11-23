import os
import subprocess
from flask import Blueprint, jsonify, current_app, request

health_bp = Blueprint("health", __name__)

CRASH_FLAG_FILE = "/tmp/devops_simulated_crash"

@health_bp.route("/healthz", methods=["GET"])
def health_check():
    """Liveness check confirming the Flask application process is alive."""
    if os.path.exists(CRASH_FLAG_FILE):
        return jsonify({
            "status": "CRITICAL",
            "service": current_app.config.get("SERVICE_NAME", "python-backend"),
            "error": "Service Failure: Gunicorn worker process terminated (Simulated Crash)",
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
            "reason": "Backend dependency offline (Simulated Crash)"
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

# Failure simulation and self-healing recovery endpoints
@health_bp.route("/api/v1/simulate/crash", methods=["POST", "GET"])
def simulate_crash():
    with open(CRASH_FLAG_FILE, "w") as f:
        f.write("CRASHED")
    return jsonify({
        "action": "simulate_crash",
        "status": "CRITICAL",
        "message": "Simulated service crash initiated. Gunicorn backend marked UNHEALTHY (503 Service Unavailable).",
        "simulated": True
    }), 200

@health_bp.route("/api/v1/simulate/recover", methods=["POST", "GET"])
def simulate_recover():
    if os.path.exists(CRASH_FLAG_FILE):
        os.remove(CRASH_FLAG_FILE)

    run_ansible = request.args.get("ansible", "").lower() == "true" or request.form.get("ansible", "").lower() == "true"
    ansible_output = None
    
    if run_ansible:
        playbook_path = "/home/ob/devops-self-healing-project/ansible/playbooks/recover_flask.yml"
        inventory_path = "/home/ob/devops-self-healing-project/ansible/inventory/hosts.ini"
        if os.path.exists(playbook_path) and os.path.exists(inventory_path):
            try:
                res = subprocess.run(
                    ["ansible-playbook", "-i", inventory_path, playbook_path],
                    capture_output=True, text=True, timeout=30
                )
                ansible_output = (res.stdout[-300:] if res.stdout else res.stderr[-300:]).strip()
            except Exception as e:
                ansible_output = f"Ansible note: {str(e)}"

    return jsonify({
        "action": "simulate_recover",
        "status": "OK",
        "message": "Self-healing recovery completed! Backend restored to 200 OK.",
        "ansible_executed": run_ansible,
        "ansible_summary": ansible_output if ansible_output else "Process state flag cleared and /healthz restored to 200 OK.",
        "simulated": False
    }), 200
