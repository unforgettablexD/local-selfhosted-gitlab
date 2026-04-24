from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

REQUEST_COUNT = Counter(
    "request_count",
    "HTTP request count",
    ["method", "path", "status_code"],
)
REQUEST_LATENCY_SECONDS = Histogram("request_latency_seconds", "HTTP request latency seconds")
PAYMENT_SUCCESS_TOTAL = Counter("payment_success_total", "Successful payment count")
PAYMENT_FAILURE_TOTAL = Counter("payment_failure_total", "Failed payment count")
QUOTE_GENERATED_TOTAL = Counter("quote_generated_total", "Generated quote count")
SEVERITY_HIGH_TOTAL = Counter("severity_high_total", "High severity evaluations")
SEVERITY_EVALUATION_TOTAL = Counter("severity_evaluation_total", "Severity evaluation count")


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
