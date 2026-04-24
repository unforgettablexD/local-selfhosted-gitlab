#!/usr/bin/env bash
set -euo pipefail

commands=(docker kubectl helm kind terraform pulumi python3 npm)
missing=0

for cmd in "${commands[@]}"; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing prerequisite: $cmd"
    missing=1
  fi
done

if [[ "$missing" -eq 1 ]]; then
  echo "Install missing tools and rerun."
  exit 1
fi

echo "All prerequisites found."
