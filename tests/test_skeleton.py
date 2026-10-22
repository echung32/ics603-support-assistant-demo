# tests/test_skeleton.py
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "<form" in response.text


def test_chat_answers_with_the_declared_fields():
    response = client.post("/chat", json={"question": "Could I get $30 back for order A-1001?"})
    assert response.status_code == 200
    assert set(response.json()) == {"answer", "refund"}
