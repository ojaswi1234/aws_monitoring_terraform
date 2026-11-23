def test_status_endpoint(client):
    """Test /api/v1/status endpoint returns valid status, version, and uptime."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data["application"] == "DevOps Self-Healing System"
    assert data["status"] == "running"
    assert data["backend"] == "Flask"
    assert data["version"] == "1.0.0"
    assert "uptime_seconds" in data
    assert isinstance(data["uptime_seconds"], (int, float))
