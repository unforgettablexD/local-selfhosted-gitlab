# Terraform Local Module

## Usage

```bash
cd infra/terraform/local
terraform init
terraform plan
terraform apply -auto-approve
```

Enable Kubernetes resource management:

```bash
terraform apply -auto-approve -var='enable_kubernetes_resources=true'
```

This local pattern maps to cloud later by replacing local-only resources with cloud providers (AWS/GCP/Azure) while keeping the same IaC workflow.
