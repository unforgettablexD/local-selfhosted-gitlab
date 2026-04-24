# Pulumi Local Example

This Pulumi program manages local Kubernetes resources using your local kind context.

## Run

```bash
cd infra/pulumi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pulumi stack init dev || true
pulumi up
```

## Local-First and Cloud Mapping

- Local now: namespace/configmap in kind.
- Cloud later: keep the same Pulumi workflow and swap provider config for managed Kubernetes clusters in AWS/GCP/Azure.
