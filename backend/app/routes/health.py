from flask import Blueprint, jsonify, current_app

health_bp = Blueprint("health", __name__)

@health_bp.route("/healthz", methods=["GET"])
def health_check():
    """Liveness check confirming the Flask application process is alive."""
    return jsonify({
        "status": "ok",
        "service": current_app.config.get("SERVICE_NAME", "python-backend"),
    }), 200

@health_bp.route("/readyz", methods=["GET"])
def readiness_check():
    """Readiness check confirming backend is prepared to serve incoming traffic."""
    # Readiness verification: ensure application config is loaded and operational
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
