Param()
$ErrorActionPreference = "Stop"

$gitlabUrl = if ($env:GITLAB_URL) { $env:GITLAB_URL } else { "http://localhost:8080" }
$runnerName = if ($env:RUNNER_NAME) { $env:RUNNER_NAME } else { "local-docker-runner" }
$registrationToken = $env:REGISTRATION_TOKEN

if (-not $registrationToken) {
  Write-Host "Set REGISTRATION_TOKEN in env before running this command." -ForegroundColor Red
  exit 1
}

docker exec -it local-gitlab-runner gitlab-runner register `
  --non-interactive `
  --url $gitlabUrl `
  --registration-token $registrationToken `
  --executor docker `
  --docker-image "python:3.11" `
  --description $runnerName `
  --docker-privileged `
  --docker-volumes /var/run/docker.sock:/var/run/docker.sock
