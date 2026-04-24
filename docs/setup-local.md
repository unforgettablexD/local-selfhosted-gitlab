# Local Setup

## Prerequisites

- Docker + Docker Compose
- Python 3.11+
- Node.js 22+
- kind
- kubectl
- Helm
- Terraform
- Pulumi

## Bootstrap

Start Docker Desktop first (required on Windows):

```powershell
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

Optional tool install with `winget`:

```powershell
winget install --id Kubernetes.kind -e
winget install --id Helm.Helm -e
winget install --id Hashicorp.Terraform -e
winget install --id Pulumi.Pulumi -e
```

Then run:

```bash
make prereqs
make app-up
make test
```

Full automatic bootstrap:

```powershell
make platform-up
```

Open local status dashboard:

- [http://localhost:4173](http://localhost:4173)

## Run platform dependencies

```bash
make kind-create
make observability-up
```

## Validate

```bash
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```
