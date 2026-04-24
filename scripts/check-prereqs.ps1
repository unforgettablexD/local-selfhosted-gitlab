Param()
$ErrorActionPreference = "Stop"

$commands = @("docker", "kubectl", "helm", "kind", "terraform", "python", "npm")
$missing = @()

foreach ($cmd in $commands) {
  if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
    $missing += $cmd
  }
}

$pulumiCmd = Get-Command pulumi -ErrorAction SilentlyContinue
if (-not $pulumiCmd) {
  $pulumiFallbacks = @(
    "C:\Program Files\Pulumi\bin\pulumi.exe",
    "C:\Program Files (x86)\Pulumi\pulumi.exe"
  )
  $pulumiFound = $false
  foreach ($path in $pulumiFallbacks) {
    if (Test-Path $path) {
      $pulumiFound = $true
      break
    }
  }
  if (-not $pulumiFound) {
    $missing += "pulumi"
  }
}

if ($missing.Count -gt 0) {
  Write-Host "Missing prerequisite(s): $($missing -join ', ')" -ForegroundColor Red
  exit 1
}

try {
  docker info *> $null
} catch {
  Write-Host "Docker is installed but daemon is not running. Start Docker Desktop and retry." -ForegroundColor Red
  exit 1
}

Write-Host "All prerequisites found and Docker daemon is reachable." -ForegroundColor Green
