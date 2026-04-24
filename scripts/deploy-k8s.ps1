Param()
$ErrorActionPreference = "Stop"

kind load docker-image platform-backend:local --name devsecops-lab
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
kubectl -n devsecops-lab rollout restart deployment/backend
kubectl -n devsecops-lab rollout status deployment/backend --timeout=180s
