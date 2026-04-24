# Terraform Local Usage

```bash
cd infra/terraform/local
terraform init
terraform plan
terraform apply -auto-approve
```

Enable Kubernetes objects:

```bash
terraform apply -auto-approve -var='enable_kubernetes_resources=true'
```

## Cloud mapping

Local providers demonstrate repeatable IaC workflows. In cloud, replace local-only resources with managed services/providers (EKS/GKE/AKS, cloud registries, secret managers).
