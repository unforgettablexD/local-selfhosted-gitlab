Param()
$ErrorActionPreference = "Stop"

if (kind get clusters | Select-String -SimpleMatch "devsecops-lab") {
  Write-Host "kind cluster devsecops-lab already exists; reusing existing cluster." -ForegroundColor Yellow
  kubectl config use-context kind-devsecops-lab | Out-Null
  kubectl cluster-info --context kind-devsecops-lab
  exit 0
}

kind create cluster --name devsecops-lab --config k8s/kind-config.yaml
kubectl cluster-info --context kind-devsecops-lab
