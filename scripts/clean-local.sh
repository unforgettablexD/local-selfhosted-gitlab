#!/usr/bin/env bash
set -euo pipefail

docker compose down -v || true
docker compose -f gitlab/docker-compose.gitlab.yml down -v || true
docker compose -f observability/docker-compose.observability.yml down -v || true
kind delete cluster --name devsecops-lab || true
