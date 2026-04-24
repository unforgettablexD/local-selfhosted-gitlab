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


def test_quote_generation():
    response = client.post(
        "/api/quotes",
        headers=auth_headers(),
        json={"org_id": "org-1", "plan": "one_time", "license_count": 2},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "quote_created"
    assert body["total"] == 398.0


def test_payment_started():
    quote = client.post(
        "/api/quotes",
        headers=auth_headers(),
        json={"org_id": "org-1", "plan": "one_time", "license_count": 1},
    ).json()
    response = client.post(
        "/api/payments/start",
        headers=auth_headers(),
        json={"quote_id": quote["quote_id"], "payment_type": "one_time"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "payment_processing"


def test_payment_success_and_license_activation():
    quote = client.post(
        "/api/quotes",
        headers=auth_headers(),
        json={"org_id": "org-1", "plan": "one_time", "license_count": 3},
    ).json()
    payment = client.post(
        "/api/payments/start",
        headers=auth_headers(),
        json={"quote_id": quote["quote_id"], "payment_type": "one_time"},
    ).json()
    webhook = client.post(
        "/api/payments/webhook",
        headers={"x-webhook-signature": "demo-valid-signature"},
        json={"payment_id": payment["payment_id"], "event": "payment_success"},
    )
    assert webhook.status_code == 200
    assert webhook.json()["license_status"] == "license_active"


def test_subscription_flow():
    quote = client.post(
        "/api/quotes",
        headers=auth_headers(),
        json={"org_id": "org-1", "plan": "subscription", "license_count": 10},
    ).json()
    payment = client.post(
        "/api/payments/start",
        headers=auth_headers(),
        json={"quote_id": quote["quote_id"], "payment_type": "subscription"},
    )
    assert payment.status_code == 200
    assert payment.json()["payment_type"] == "subscription"


def test_license_suspension():
    quote = client.post(
        "/api/quotes",
        headers=auth_headers(),
        json={"org_id": "org-1", "plan": "subscription", "license_count": 5},
    ).json()
    payment = client.post(
        "/api/payments/start",
        headers=auth_headers(),
        json={"quote_id": quote["quote_id"], "payment_type": "subscription"},
    ).json()
    webhook = client.post(
        "/api/payments/webhook",
        headers={"x-webhook-signature": "demo-valid-signature"},
        json={"payment_id": payment["payment_id"], "event": "license_suspended"},
    )
    assert webhook.status_code == 200
    assert webhook.json()["license_status"] == "license_suspended"


def test_franchise_multi_license_distribution():
    quote = client.post(
        "/api/quotes",
        headers=auth_headers(),
        json={"org_id": "org-1", "plan": "one_time", "license_count": 10},
    ).json()
    response = client.post(
        "/api/payments/start",
        headers=auth_headers(),
        json={
            "quote_id": quote["quote_id"],
            "payment_type": "one_time",
            "franchise_distribution": {"org-1": 4, "org-2": 6},
        },
    )
    assert response.status_code == 200
    assert response.json()["franchise_distribution"]["org-2"] == 6


def test_webhook_signature_placeholder_validation():
    quote = client.post(
        "/api/quotes",
        headers=auth_headers(),
        json={"org_id": "org-1", "plan": "one_time", "license_count": 1},
    ).json()
    payment = client.post(
        "/api/payments/start",
        headers=auth_headers(),
        json={"quote_id": quote["quote_id"], "payment_type": "one_time"},
    ).json()
    webhook = client.post(
        "/api/payments/webhook",
        headers={"x-webhook-signature": "bad"},
        json={"payment_id": payment["payment_id"], "event": "payment_success"},
    )
    assert webhook.status_code == 401
