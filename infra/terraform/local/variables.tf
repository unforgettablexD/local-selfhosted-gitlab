variable "project_name" {
  type        = string
  description = "Project identifier."
  default     = "local-selfhosted-gitlab"
}

variable "kubeconfig_path" {
  type        = string
  description = "Path to kubeconfig."
  default     = "~/.kube/config"
}

variable "kube_context" {
  type        = string
  description = "Kubernetes context name."
  default     = "kind-devsecops-lab"
}

variable "namespace" {
  type        = string
  description = "Namespace managed by Terraform."
  default     = "tf-managed-lab"
}

variable "enable_kubernetes_resources" {
  type        = bool
  description = "Toggle for local Kubernetes resources."
  default     = false
}

