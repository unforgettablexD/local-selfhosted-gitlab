# Setup Local GitLab Runner

## Verify Runner Container

```bash
docker compose -f gitlab/docker-compose.gitlab.yml ps
```

## Register Docker Executor Runner

```bash
export REGISTRATION_TOKEN="<replace-with-project-token>"
bash gitlab/runner/register-runner.sh
```

## Runner Validation

1. In GitLab, open `Settings` -> `CI/CD` -> `Runners`.
2. Confirm runner status is `online`.
3. Trigger a pipeline and verify jobs are picked by the runner.

## Notes

- This runner mounts `/var/run/docker.sock` for Docker-in-Docker style jobs.
- For stricter security in real production, isolate runners by trust boundary and use protected runners/tags.
