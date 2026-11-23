def test_landing_endpoint(client):
    """Test / root endpoint returns overview of backend, reverse proxy, and monitoring."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data["project"] == "DevOps Self-Healing System"
    assert data["framework"] == "Python Flask (WSGI)"
    assert data["server"] == "Gunicorn"
    assert data["reverse_proxy"] == "Nginx"
    assert "endpoints" in data

def test_info_endpoint(client):
    """Test /api/v1/info endpoint returns safe non-sensitive metadata."""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data["service"] == "python-backend"
    assert data["application"] == "DevOps Self-Healing System"
    assert "environment" in data
    assert data["version"] == "1.0.0"
    # Ensure sensitive items are NOT present
    for sensitive_key in ["password", "secret", "private_ip", "aws_key"]:
        assert sensitive_key not in data

def test_metrics_endpoint(client):
    """Test /api/v1/metrics endpoint returns request counts and uptime."""
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert "uptime_seconds" in data
    assert "total_requests" in data
    assert data["total_requests"] >= 1

def test_not_found_handler(client):
    """Test 404 handler returns standardized JSON."""
    response = client.get("/non-existent-route")
    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert data["error"] == "Not Found"
