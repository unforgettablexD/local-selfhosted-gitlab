Param(
  [switch]$SkipGitLab,
  [switch]$SkipSecurity
)
$ErrorActionPreference = "Stop"

function Invoke-Step {
  param([string]$Cmd)
  Invoke-Expression $Cmd
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed: $Cmd"
  }
}

Write-Host "==> Checking prerequisites" -ForegroundColor Cyan
Invoke-Step "powershell -ExecutionPolicy Bypass -File scripts/check-prereqs.ps1"

Write-Host "==> Starting app stack" -ForegroundColor Cyan
Invoke-Step "docker compose up -d --build"

Write-Host "==> Running tests" -ForegroundColor Cyan
Invoke-Step "powershell -ExecutionPolicy Bypass -File scripts/test-all.ps1"

if (-not $SkipSecurity) {
  Write-Host "==> Running security checks" -ForegroundColor Cyan
  Invoke-Step "powershell -ExecutionPolicy Bypass -File scripts/test-all.ps1 security"
}

Write-Host "==> Starting observability" -ForegroundColor Cyan
Invoke-Step "docker compose -f observability/docker-compose.observability.yml up -d"

Write-Host "==> Ensuring kind cluster + k8s deployment" -ForegroundColor Cyan
Invoke-Step "powershell -ExecutionPolicy Bypass -File scripts/create-kind-cluster.ps1"
Invoke-Step "powershell -ExecutionPolicy Bypass -File scripts/deploy-k8s.ps1"
Invoke-Step "powershell -ExecutionPolicy Bypass -File scripts/deploy-helm.ps1 dev"
Invoke-Step "powershell -ExecutionPolicy Bypass -File scripts/deploy-helm.ps1 staging"
Invoke-Step "powershell -ExecutionPolicy Bypass -File scripts/deploy-helm.ps1 prod"

if (-not $SkipGitLab) {
  Write-Host "==> Starting local GitLab + Runner" -ForegroundColor Cyan
  Invoke-Step "docker compose -f gitlab/docker-compose.gitlab.yml up -d"
}

Write-Host "==> Starting local status dashboard" -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
  "-NoProfile",
  "-NoExit",
  "-Command",
  "Set-Location '$PWD'; npm --prefix app/frontend start"
) | Out-Null

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Platform bootstrap complete." -ForegroundColor Green
Write-Host "Dashboard: http://localhost:4173" -ForegroundColor Green
Write-Host "Backend docs: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Prometheus: http://localhost:9090" -ForegroundColor Green
Write-Host "Grafana: http://localhost:3000" -ForegroundColor Green
if (-not $SkipGitLab) {
  Write-Host "GitLab: http://localhost:8080 (may need extra warm-up time)" -ForegroundColor Yellow
}

Start-Process "http://localhost:4173"
