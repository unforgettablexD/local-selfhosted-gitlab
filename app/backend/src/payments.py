from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from .metrics import PAYMENT_FAILURE_TOTAL, PAYMENT_SUCCESS_TOTAL, QUOTE_GENERATED_TOTAL

PAYMENT_STATES = {
    "quote_created",
    "payment_started",
    "payment_processing",
    "payment_success",
    "license_active",
    "license_suspended",
    "license_inactive",
}


@dataclass
class Quote:
    quote_id: str
    org_id: str
    plan: str
    license_count: int
    unit_price: float
    total: float
    status: str = "quote_created"


@dataclass
class Payment:
    payment_id: str
    quote_id: str
    org_id: str
    payment_type: str
    franchise_distribution: dict[str, int] = field(default_factory=dict)
    status: str = "payment_started"
    license_status: str = "license_inactive"


QUOTES: dict[str, Quote] = {}
PAYMENTS: dict[str, Payment] = {}


def reset_payments() -> None:
    QUOTES.clear()
    PAYMENTS.clear()


def create_quote(org_id: str, plan: str, license_count: int) -> Quote:
    unit_price = 49.0 if plan == "subscription" else 199.0
    total = unit_price * license_count
    quote = Quote(
        quote_id=f"qt-{uuid4().hex[:8]}",
        org_id=org_id,
        plan=plan,
        license_count=license_count,
        unit_price=unit_price,
        total=total,
    )
    QUOTES[quote.quote_id] = quote
    QUOTE_GENERATED_TOTAL.inc()
    return quote


def start_payment(
    quote_id: str,
    payment_type: str,
    org_id: str,
    franchise_distribution: dict[str, int] | None = None,
) -> Payment:
    _ = QUOTES[quote_id]
    payment = Payment(
        payment_id=f"pay-{uuid4().hex[:8]}",
        quote_id=quote_id,
        org_id=org_id,
        payment_type=payment_type,
        franchise_distribution=franchise_distribution or {},
    )
    payment.status = "payment_processing"
    PAYMENTS[payment.payment_id] = payment
    return payment


def apply_payment_webhook(payment_id: str, event: str) -> Payment:
    payment = PAYMENTS[payment_id]
    if event == "payment_success":
        payment.status = "payment_success"
        payment.license_status = "license_active"
        PAYMENT_SUCCESS_TOTAL.inc()
    elif event == "payment_failed":
        payment.status = "license_inactive"
        payment.license_status = "license_inactive"
        PAYMENT_FAILURE_TOTAL.inc()
    elif event == "license_suspended":
        payment.status = "license_suspended"
        payment.license_status = "license_suspended"
    elif event == "license_inactive":
        payment.status = "license_inactive"
        payment.license_status = "license_inactive"
    return payment
