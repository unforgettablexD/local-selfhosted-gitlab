from fastapi.testclient import TestClient

from src.auth import reset_orgs
from src.main import app
from src.payments import reset_payments

client = TestClient(app)


def auth_headers(role: str = "billing", org_id: str = "org-1"):
    return {"x-user-id": "u-1", "x-role": role, "x-org-id": org_id}


def setup_function():
    reset_orgs()
    reset_payments()


def test_org_based_access_control():
    response = client.post(
        "/api/quotes",
        headers=auth_headers(org_id="org-1"),
        json={"org_id": "org-2", "plan": "one_time", "license_count": 1},
    )
    assert response.status_code == 403


def test_admin_api_not_public():
    response = client.get("/api/admin/orgs", headers=auth_headers(role="billing"))
    assert response.status_code == 403


def test_admin_can_manage_orgs():
    create_resp = client.post(
        "/api/admin/orgs",
        headers=auth_headers(role="admin"),
        json={"org_id": "org-9", "name": "NewCo"},
    )
    assert create_resp.status_code == 200

    list_resp = client.get("/api/admin/orgs", headers=auth_headers(role="admin"))
    assert list_resp.status_code == 200
    assert any(org["id"] == "org-9" for org in list_resp.json()["orgs"])
