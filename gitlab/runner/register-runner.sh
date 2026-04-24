#!/usr/bin/env bash
set -euo pipefail

GITLAB_URL="${GITLAB_URL:-http://host.docker.internal:8929}"
RUNNER_CLONE_URL="${RUNNER_CLONE_URL:-http://host.docker.internal:8929}"
RUNNER_NAME="${RUNNER_NAME:-local-docker-runner}"
REGISTRATION_TOKEN="${REGISTRATION_TOKEN:-REPLACE_ME}"

if [[ "$REGISTRATION_TOKEN" == "REPLACE_ME" ]]; then
  echo "Set REGISTRATION_TOKEN with your project or instance runner token."
  exit 1
fi

if [[ "$REGISTRATION_TOKEN" == glrt-* ]]; then
  TOKEN_ARG="--token"
else
  TOKEN_ARG="--registration-token"
fi

docker exec -it local-gitlab-runner gitlab-runner register \
  --non-interactive \
  --url "${GITLAB_URL}" \
  ${TOKEN_ARG} "${REGISTRATION_TOKEN}" \
  --clone-url "${RUNNER_CLONE_URL}" \
  --executor docker \
  --docker-image "python:3.11" \
  --description "${RUNNER_NAME}" \
  --docker-privileged \
  --docker-volumes /var/run/docker.sock:/var/run/docker.sock
