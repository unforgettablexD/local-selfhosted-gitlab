# self-hosted-gitlab-devsecops-platform

Production-style, **free/local-first** DevSecOps lab proving self-hosted platform ownership across GitLab CE, CI/CD, Kubernetes, Helm, Terraform, Pulumi, security scanning, and observability.

No paid cloud required. Everything runs on a developer laptop with Docker, kind, Helm, Terraform, and Pulumi.

## What This Proves For DevSecOps Roles

- Operate and secure **self-hosted GitLab + Runner**.
- Design multi-stage **CI/CD** with quality, security, build, and controlled deployment gates.
- Run **Kubernetes-native releases** via raw manifests and Helm.
- Implement **IaC** using both Terraform and Pulumi (local-first patterns that map to AWS/GCP).
- Build **secure-by-default services** with RBAC, org isolation, and deterministic security scans.
- Run **observability + ops runbooks** for incident response and backup/restore.

## Architecture

```mermaid
flowchart LR
  Dev[Developer Laptop] --> GL[GitLab CE - Docker Compose]
  Dev --> Runner[GitLab Runner - Docker Executor]
  Runner --> Pipeline[GitLab CI Pipeline]
  Pipeline --> Sec[Security Jobs: Bandit/Gitleaks/Trivy/Audit]
  Pipeline --> Build[Docker Build/Push]
  Pipeline --> Helm[Helm Deploy]
  Helm --> K8s[kind Kubernetes Cluster]
  K8s --> App[FastAPI Backend]
  App --> Metrics[/metrics Prometheus]
  Prom[Prometheus] --> Grafana[Grafana Dashboards]
  App --> Redis[(Redis)]
  App --> Worker[Celery Worker]
  TF[Terraform Local] --> K8s
  Pulumi[Pulumi Python] --> K8s
```

## Quick Start

```bash
make prereqs
make app-up
make test
make kind-create
make k8s-deploy
make observability-up
```

One-command bootstrap (Windows PowerShell):

```powershell
make platform-up
```

Status dashboard (clickable links + live health checks): [http://localhost:4173](http://localhost:4173)

- Backend: [http://localhost:8000](http://localhost:8000)
- GitLab: [http://localhost:8080](http://localhost:8080)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000) (`admin` / `admin`)

## FastAPI Service Endpoints

- `GET /health`
- `GET /metrics`
- `POST /api/quotes`
- `POST /api/payments/start`
- `POST /api/payments/webhook`
- `POST /api/severity/evaluate`
- `GET /api/admin/orgs`
- `POST /api/admin/orgs`
- `DELETE /api/admin/orgs/{org_id}`

## Local GitLab + Runner

```bash
make gitlab-up
make runner-register
```

Detailed instructions:
- [docs/setup-gitlab-local.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/docs/setup-gitlab-local.md)
- [docs/setup-runner-local.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/docs/setup-runner-local.md)

## CI/CD Pipeline

Stages:
- `lint`
- `test`
- `security`
- `build`
- `package`
- `deploy_staging`
- `deploy_prod` (manual)

Reference:
- [.gitlab-ci.yml](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/.gitlab-ci.yml)
- [docs/ci-cd-pipeline.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/docs/ci-cd-pipeline.md)

## Kubernetes + Helm

Raw manifests:
- [k8s/](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/k8s)

Helm chart:
- [helm/backend/](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/helm/backend)

Commands:

```bash
make kind-create
make k8s-deploy
make helm-deploy-dev
make helm-deploy-staging
```


## Terraform and Pulumi (Local-First)

- Terraform: [infra/terraform/local/README.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/infra/terraform/local/README.md)
- Pulumi: [infra/pulumi/README.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/infra/pulumi/README.md)

## Security Scanning

Included checks:
- Python dependency audit (`pip-audit`)
- Node dependency audit (`npm audit`)
- SAST (`bandit`)
- Secret scanning (`gitleaks`)
- Container scanning (`trivy`)
- Custom admin endpoint exposure validation

Details:
- [docs/security-scanning.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/docs/security-scanning.md)

## Observability

Prometheus scrapes backend metrics; Grafana dashboards show request rate, latency, errors, payment outcomes, quote volume, severity distribution, and health.

- [docs/observability.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/docs/observability.md)

## Backup / Restore and Incident Ops

- [docs/backup-restore-runbook.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/docs/backup-restore-runbook.md)
- [docs/incident-runbook.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/docs/incident-runbook.md)

## Resume-Ready Bullets

- [docs/resume-bullets.md](/C:/Users/akkil/OneDrive/Desktop/codes/zacalar/docs/resume-bullets.md)

## Public Safety Notes

- No real secrets are committed.
- `secret.example.yaml` contains fake placeholders only.
- Payment flow is mocked; no Stripe keys, no external payment processing.
- Demo data is in-memory and synthetic.
