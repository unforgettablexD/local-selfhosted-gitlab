# Pulumi Local Usage

```bash
cd infra/pulumi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pulumi stack init dev || true
pulumi up
```

Pulumi manages local kind namespace/configmap resources without paid cloud dependencies.

## Cloud mapping

Retain the same Pulumi program structure and switch provider configuration to managed cloud Kubernetes clusters.
