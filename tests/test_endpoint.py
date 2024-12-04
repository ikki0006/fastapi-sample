from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_reception_endpoint() -> None:
    response = client.post(
        "/api/v1/reception",
        json={
            "session_id": 11111,
            "polling": True,
            "data": {"model": "sonet", "path": "sample", "prompt": {"test": "test"}},
        },
    )
    assert response.status_code == 200
    assert response.json()["session_id"] == 11111
    assert response.json()["result"]["id"] is not None
    return None
