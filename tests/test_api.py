from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_devuelve_estructura_correcta():
    payload = {f"V{i}": 0.0 for i in range(1, 29)}
    payload.update({"Time": 0.0, "Amount": 100.0})

    response = client.post("/predict", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "is_fraud" in data
    assert "fraud_probability" in data
    assert "risk_level" in data
    assert 0 <= data["fraud_probability"] <= 1


def test_predict_rechaza_monto_negativo():
    payload = {f"V{i}": 0.0 for i in range(1, 29)}
    payload.update({"Time": 0.0, "Amount": -50.0})

    response = client.post("/predict", json=payload)
    assert response.status_code == 422
