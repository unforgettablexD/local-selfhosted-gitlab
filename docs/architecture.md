# Architecture

## Platform Components

- Self-hosted GitLab CE and GitLab Runner via Docker Compose.
- FastAPI backend + Redis + Celery worker.
- Local Kubernetes cluster with kind.
- Helm release management across dev/staging/prod values.
- Terraform and Pulumi local-first IaC examples.
- Prometheus + Grafana for observability.
- Security scans integrated in GitLab pipeline.

## Data and Control Flow

1. Developer pushes code to GitLab.
2. Runner executes lint/test/security/build/package stages.
3. Staging and prod deployments run through Helm with namespace separation.
4. Backend exports metrics to Prometheus; Grafana visualizes SLO/SLI panels.
5. Ops workflows use backup and incident runbooks.

## Security Model

- Header-based RBAC and org boundaries for demo APIs.
- Admin routes protected via `require_admin_user`.
- Cross-org requests denied for non-admin users.
- Webhook endpoint enforces signature placeholder validation.
