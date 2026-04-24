# Kubernetes Local (kind)

## Create cluster

```bash
make kind-create
kubectl get nodes
```

## Deploy raw manifests

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.example.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
```

## Validate rollout

```bash
kubectl -n devsecops-lab get deploy,pods,svc,hpa
kubectl -n devsecops-lab rollout status deploy/backend
```
