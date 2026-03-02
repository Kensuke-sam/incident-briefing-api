from __future__ import annotations

from fastapi.testclient import TestClient


def test_workflow(client: TestClient, auth_headers: dict[str, str]) -> None:
    payload = {
        "service_name": "checkout-api",
        "alert_summary": "5xx rate exceeded threshold",
        "timeline": "09:02 API latency spiked. 09:05 checkout started returning 502. 09:12 "
        "rollback initiated.",
    }
    create_response = client.post(
        "/incidents",
        json=payload,
        headers=auth_headers,
    )
    assert create_response.status_code == 201

    record_id = create_response.json()["id"]
    analysis_response = client.post(
        f"/incidents/{record_id}/brief",
        headers=auth_headers,
    )
    assert analysis_response.status_code == 200
    assert analysis_response.json()["severity"] == "sev1"

    get_response = client.get(
        f"/incidents/{record_id}/briefing",
        headers=auth_headers,
    )
    assert get_response.status_code == 200
