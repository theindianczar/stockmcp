from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    """Test the health endpoint returns correct response."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
