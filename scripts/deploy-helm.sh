#!/usr/bin/env bash
set -euo pipefail

env="${1:-dev}"
values_file="helm/backend/values-${env}.yaml"
namespace="${env}"

kind load docker-image platform-backend:local --name devsecops-lab
helm upgrade --install platform-backend helm/backend \
  --namespace "${namespace}" \
  --create-namespace \
  -f helm/backend/values.yaml \
  -f "${values_file}"
