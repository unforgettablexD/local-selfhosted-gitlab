locals {
  generated_path = "${path.module}/generated/${var.project_name}.tfvars.json"
}

resource "local_file" "platform_metadata" {
  filename = local.generated_path
  content = jsonencode({
    project   = var.project_name
    namespace = var.namespace
    context   = var.kube_context
  })
}

resource "null_resource" "iac_run_marker" {
  triggers = {
    generated_file = local_file.platform_metadata.filename
    generated_hash = local_file.platform_metadata.content_md5
  }

  provisioner "local-exec" {
    command = "echo Terraform local run complete for ${var.project_name}"
  }
}

resource "kubernetes_namespace" "lab" {
  count = var.enable_kubernetes_resources ? 1 : 0
  metadata {
    name = var.namespace
    labels = {
      managed-by = "terraform"
    }
  }
}

resource "kubernetes_config_map" "lab_config" {
  count = var.enable_kubernetes_resources ? 1 : 0
  metadata {
    name      = "platform-config"
    namespace = kubernetes_namespace.lab[0].metadata[0].name
  }
  data = {
    app_env = "terraform-local"
  }
}
