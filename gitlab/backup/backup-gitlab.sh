#!/usr/bin/env bash
set -euo pipefail

timestamp="$(date +%Y%m%d-%H%M%S)"
backup_dir="${1:-./gitlab/backup/artifacts}"

mkdir -p "${backup_dir}"

docker exec local-gitlab-ce gitlab-backup create STRATEGY=copy
docker cp local-gitlab-ce:/var/opt/gitlab/backups "${backup_dir}/gitlab-backups-${timestamp}"
docker cp local-gitlab-ce:/etc/gitlab "${backup_dir}/gitlab-config-${timestamp}"

echo "Backup complete in ${backup_dir}"
