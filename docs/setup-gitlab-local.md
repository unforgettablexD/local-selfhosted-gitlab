# Setup Self-Hosted GitLab Locally

## Start GitLab CE + Runner Containers

```bash
make gitlab-up
docker compose -f gitlab/docker-compose.gitlab.yml ps
```

GitLab UI: [http://localhost:8080](http://localhost:8080)

## Retrieve Initial Root Password

```bash
docker exec local-gitlab-ce cat /etc/gitlab/initial_root_password
```

Use `root` and the printed password to log in.

## Create a GitLab Project

1. Sign in to `http://localhost:8080`.
2. Create a new blank project named `local-selfhosted-gitlab`.
3. Add your repository remote and push:

```bash
git init
git remote add origin http://localhost:8080/root/local-selfhosted-gitlab.git
git add .
git commit -m "Initial DevSecOps lab"
git push -u origin main
```

## Register Local Runner

Get runner registration token from project settings:

- `Settings` -> `CI/CD` -> `Runners` -> `New project runner`.

Register:

```powershell
$env:REGISTRATION_TOKEN="<token>"
make runner-register
```

## Mirror/Import Project

Use GitLab project `Settings` -> `Repository` -> `Mirroring repositories` to mirror from GitHub, or use project import from URL.

## Trigger Pipeline

- Push a commit or open a merge request.
- Visit `CI/CD` -> `Pipelines`.

