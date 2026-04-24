#!/usr/bin/env bash
set -euo pipefail

mode="${1:-all}"

pushd app/backend >/dev/null
python3 -m pip install -r requirements.txt >/dev/null

if [[ "$mode" == "security" ]]; then
  ruff check src tests
  python3 -m bandit -c ../../security/bandit.yaml -r src
  python3 -m pip_audit -r requirements.txt
else
  ruff check src tests
  pytest -q
fi
popd >/dev/null

if [[ "$mode" != "security" ]]; then
  pushd app/frontend >/dev/null
  npm test
  popd >/dev/null
fi

if [[ "$mode" == "security" ]]; then
  python3 security/api_exposure_check.py
fi
