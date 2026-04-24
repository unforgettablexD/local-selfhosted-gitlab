output "generated_metadata_file" {
  value = local_file.platform_metadata.filename
}

output "namespace_name" {
  value       = var.enable_kubernetes_resources ? kubernetes_namespace.lab[0].metadata[0].name : "disabled"
  description = "Namespace managed by Terraform when enabled."
}
