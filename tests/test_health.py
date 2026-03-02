from __future__ import annotations

from fastapi.testclient import TestClient


def test_healthz(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_protected_route_requires_api_key(client: TestClient) -> None:
    payload = {
        "service_name": "checkout-api",
        "alert_summary": "5xx rate exceeded threshold",
        "timeline": "09:02 API latency spiked. 09:05 checkout started returning 502. 09:12 "
        "rollback initiated.",
    }
    response = client.post("/incidents", json=payload)
    assert response.status_code == 401
