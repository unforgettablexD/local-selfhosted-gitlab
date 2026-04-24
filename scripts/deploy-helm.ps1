Param(
  [string]$Env = "dev"
)
$ErrorActionPreference = "Stop"

$valuesFile = "helm/backend/values-$Env.yaml"
$namespace = $Env

kind load docker-image platform-backend:local --name devsecops-lab
helm upgrade --install platform-backend helm/backend `
  --namespace $namespace `
  --create-namespace `
  -f helm/backend/values.yaml `
  -f $valuesFile
