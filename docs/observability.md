# Observability

## Start stack

```bash
make observability-up
```

- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (`admin/admin`)

## Exposed metrics

- `request_count`
- `request_latency_seconds`
- `payment_success_total`
- `payment_failure_total`
- `quote_generated_total`
- `severity_high_total`
- `severity_evaluation_total`

## Dashboard panels

- request rate
- latency
- error count
- payment success/failure
- quote generation
- severity distribution
- service health
