from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_reception_endpoint():
    response = client.get("/api/v1/reception")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
