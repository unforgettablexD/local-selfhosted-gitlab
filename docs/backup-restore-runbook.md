# Backup and Restore Runbook

## Scope

- Git repositories
- PostgreSQL/internal metadata in GitLab backup archive
- GitLab configuration from `/etc/gitlab`
- Local equivalent of object storage: versioned backup directory on disk
- Runner configuration backups

## RTO / RPO assumptions

- RTO: 2 hours (single-node local restore target)
- RPO: 24 hours (daily scheduled backup baseline)

## Backup procedure

```bash
bash gitlab/backup/backup-gitlab.sh ./gitlab/backup/artifacts
```

Artifacts captured:

- GitLab backup tar from `/var/opt/gitlab/backups`
- GitLab config from `/etc/gitlab`

## Secrets backup

- Back up GitLab secrets (`gitlab-secrets.json`) and CI variables export process docs separately.
- Do not commit real secrets; keep encrypted offline copies.

## Restore procedure

1. Stand up GitLab container with matching version.
2. Place backup archive into `/var/opt/gitlab/backups`.
3. Run:

```bash
bash gitlab/backup/restore-gitlab.sh <backup_id>
```

4. Restore `/etc/gitlab` config and restart.
5. Validate:
- Can log in as admin
- Projects/repositories present
- Pipelines and runner registration operational

## Test restore cadence

- Run restore test monthly in isolated local environment.
- Record restore duration and issues in ops notes.
