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

PowerShell:

```powershell
$env:REGISTRATION_TOKEN="<replace-with-project-token>"
make runner-register
```

## Runner Validation

1. In GitLab, open `Settings` -> `CI/CD` -> `Runners`.
2. Confirm runner status is `online`.
3. Ensure `Run untagged jobs` is enabled unless every job in `.gitlab-ci.yml` has explicit tags.
4. Trigger a pipeline and verify jobs are picked by the runner.

## Notes

- This runner mounts `/var/run/docker.sock` for Docker-in-Docker style jobs.
- For stricter security in real production, isolate runners by trust boundary and use protected runners/tags.
- The registration script sets `url=http://gitlab:8929` so runner API/artifact traffic stays on the Docker network.
- The registration script sets `clone_url=http://host.docker.internal:8929` so job containers can clone from the host-mapped GitLab port on Docker Desktop.
