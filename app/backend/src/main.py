from __future__ import annotations

import time
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, Response, status
from pydantic import BaseModel, Field

from .auth import ORGS, UserContext, assert_org_access, get_current_user, require_admin_user
from .logging_config import configure_logging
from .metrics import REQUEST_COUNT, REQUEST_LATENCY_SECONDS, metrics_response
from .payments import (
    PAYMENT_STATES,
    PAYMENTS,
    QUOTES,
    apply_payment_webhook,
    create_quote,
    start_payment,
)
from .severity import evaluate_severity

configure_logging()
app = FastAPI(title="Self-Hosted DevSecOps Platform Demo", version="0.1.0")


class QuoteRequest(BaseModel):
    org_id: str
    plan: str = Field(pattern="^(one_time|subscription)$")
    license_count: int = Field(ge=1, le=10000)


class PaymentStartRequest(BaseModel):
    quote_id: str
    payment_type: str = Field(pattern="^(one_time|subscription)$")
    franchise_distribution: dict[str, int] = Field(default_factory=dict)


class WebhookRequest(BaseModel):
    payment_id: str
    event: str


class SeverityRequest(BaseModel):
    summary: str
    modifiers: list[str] = Field(default_factory=list)


class OrgRequest(BaseModel):
    org_id: str
    name: str


@app.middleware("http")
async def request_metrics_middleware(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    latency = time.perf_counter() - start
    REQUEST_LATENCY_SECONDS.observe(latency)
    REQUEST_COUNT.labels(
        method=request.method,
        path=request.url.path,
        status_code=str(response.status_code),
    ).inc()
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    return metrics_response()


@app.post("/api/quotes")
def create_quote_endpoint(
    payload: QuoteRequest,
    user: UserContext = Depends(get_current_user),
) -> dict[str, Any]:
    assert_org_access(payload.org_id, user)
    if payload.org_id not in ORGS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown org")
    quote = create_quote(payload.org_id, payload.plan, payload.license_count)
    return quote.__dict__


@app.post("/api/payments/start")
def start_payment_endpoint(
    payload: PaymentStartRequest, user: UserContext = Depends(get_current_user)
) -> dict[str, Any]:
    if payload.quote_id not in QUOTES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown quote")
    quote = QUOTES[payload.quote_id]
    assert_org_access(quote.org_id, user)

    if payload.franchise_distribution:
        distributed_total = sum(payload.franchise_distribution.values())
        if distributed_total > quote.license_count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Franchise distribution exceeds purchased licenses",
            )

    # Real integration would create a Stripe PaymentIntent/Checkout session here.
    payment = start_payment(
        quote_id=payload.quote_id,
        payment_type=payload.payment_type,
        org_id=quote.org_id,
        franchise_distribution=payload.franchise_distribution,
    )
    return payment.__dict__


@app.post("/api/payments/webhook")
def payment_webhook(
    payload: WebhookRequest,
    x_webhook_signature: str | None = Header(default=None),
) -> dict[str, Any]:
    if x_webhook_signature != "demo-valid-signature":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature",
        )
    if payload.payment_id not in PAYMENTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown payment")
    if payload.event not in PAYMENT_STATES and payload.event != "payment_failed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown payment event")

    payment = apply_payment_webhook(payload.payment_id, payload.event)
    return payment.__dict__


@app.post("/api/severity/evaluate")
def evaluate_severity_endpoint(
    payload: SeverityRequest, user: UserContext = Depends(get_current_user)
) -> dict[str, Any]:
    result = evaluate_severity(payload.summary, payload.modifiers)
    return {
        "org_id": user.org_id,
        "score": result.score,
        "level": result.level,
        "route": result.route,
    }


@app.get("/api/admin/orgs")
def list_orgs(_: UserContext = Depends(require_admin_user)) -> dict[str, Any]:
    return {"orgs": list(ORGS.values())}


@app.post("/api/admin/orgs")
def create_org(payload: OrgRequest, _: UserContext = Depends(require_admin_user)) -> dict[str, Any]:
    if payload.org_id in ORGS:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Org already exists")
    ORGS[payload.org_id] = {"id": payload.org_id, "name": payload.name}
    return ORGS[payload.org_id]


@app.delete("/api/admin/orgs/{org_id}")
def delete_org(org_id: str, _: UserContext = Depends(require_admin_user)) -> dict[str, str]:
    if org_id not in ORGS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown org")
    del ORGS[org_id]
    return {"deleted": org_id}
