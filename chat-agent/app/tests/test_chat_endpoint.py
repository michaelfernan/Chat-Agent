from fastapi.testclient import TestClient
from app.main import app


def test_chat_endpoint_works():
    with TestClient(app) as client:
        resp = client.post("/chat", json={"message": "Quanto é 2 * 3?"})
        assert resp.status_code == 200
        body = resp.json()
        assert "response" in body
        assert isinstance(body["response"], str)
