from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_device_push_and_list():
    payload = {
        "devices": [
            {
                "device_id": "asset-1",
                "hostname": "app-1",
                "device_type": "server",
                "platform": "linux",
                "vendor": "canonical",
                "product": "nginx",
                "version": "1.0",
                "business_unit": "apps",
                "owner": "ops",
                "identity_provider": "entra",
                "tags": ["prod"],
            }
        ]
    }

    push_response = client.post("/api/devices/push", json=payload)
    assert push_response.status_code == 200
    assert push_response.json()["accepted"] == 1

    list_response = client.get("/api/devices")
    assert list_response.status_code == 200
    body = list_response.json()
    assert body["total"] >= 1
    assert any(item["device_id"] == "asset-1" for item in body["items"])
