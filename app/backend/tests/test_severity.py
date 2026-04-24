from fastapi.testclient import TestClient

from src.auth import reset_orgs
from src.main import app
from src.payments import reset_payments

client = TestClient(app)


def auth_headers(role: str = "analyst", org_id: str = "org-1"):
    return {"x-user-id": "u-1", "x-role": role, "x-org-id": org_id}


def setup_function():
    reset_orgs()
    reset_payments()


def test_severity_scoring():
    response = client.post(
        "/api/severity/evaluate",
        headers=auth_headers(),
        json={"summary": "Minor known issue", "modifiers": ["known_issue"]},
    )
    assert response.status_code == 200
    assert response.json()["level"] == "low"


def test_severity_escalation():
    response = client.post(
        "/api/severity/evaluate",
        headers=auth_headers(),
        json={
            "summary": "Critical ransomware breach with privilege escalation",
            "modifiers": ["production", "customer_impact"],
        },
    )
    assert response.status_code == 200
    assert response.json()["level"] == "high"
    assert "page-on-call" in response.json()["route"]
