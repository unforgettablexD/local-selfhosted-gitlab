#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <backup_tar_id_without__gitlab_backup.tar>"
  exit 1
fi

backup_id="$1"

docker exec local-gitlab-ce gitlab-ctl stop puma
docker exec local-gitlab-ce gitlab-ctl stop sidekiq
docker exec local-gitlab-ce gitlab-backup restore BACKUP="${backup_id}" force=yes
docker exec local-gitlab-ce gitlab-ctl restart

echo "Restore completed for backup ${backup_id}"
