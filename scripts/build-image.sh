#!/usr/bin/env bash
set -euo pipefail

tag="${1:-local}"
docker build -t "platform-backend:${tag}" app/backend
