Param()
$ErrorActionPreference = "Stop"

$gitlabUrl = if ($env:GITLAB_URL) { $env:GITLAB_URL } else { "http://gitlab:8929" }
$runnerName = if ($env:RUNNER_NAME) { $env:RUNNER_NAME } else { "local-docker-runner" }
$registrationToken = $env:REGISTRATION_TOKEN

if (-not $registrationToken) {
  Write-Host "Set REGISTRATION_TOKEN in env before running this command." -ForegroundColor Red
  exit 1
}

$tokenArg = if ($registrationToken.StartsWith("glrt-")) { "--token" } else { "--registration-token" }

docker exec local-gitlab-runner gitlab-runner register `
  --non-interactive `
  --url $gitlabUrl `
  $tokenArg $registrationToken `
  --executor docker `
  --docker-image "python:3.11" `
  --description $runnerName `
  --docker-privileged `
  --docker-volumes /var/run/docker.sock:/var/run/docker.sock
