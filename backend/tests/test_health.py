def test_healthz_endpoint(client):
    """Test /healthz liveness endpoint returns HTTP 200 and expected payload."""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "python-backend"

def test_readyz_endpoint(client):
    """Test /readyz readiness endpoint returns HTTP 200 and ready state."""
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data["status"] == "ready"
    assert data["ready"] is True
    assert data["service"] == "python-backend"
