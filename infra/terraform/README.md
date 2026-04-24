# Terraform Local IaC

This folder demonstrates local-first Terraform patterns with no paid cloud dependency.

- `local/` uses `local`, `null`, and optional `kubernetes` providers.
- By default it only writes local artifacts and run markers.
- Enable Kubernetes resources by setting `enable_kubernetes_resources=true`.
