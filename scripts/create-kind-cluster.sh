#!/usr/bin/env bash
set -euo pipefail

kind create cluster --name devsecops-lab --config k8s/kind-config.yaml
kubectl cluster-info --context kind-devsecops-lab
