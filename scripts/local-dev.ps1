Param()
$ErrorActionPreference = "Stop"

docker compose up -d --build
Write-Host "Backend: http://localhost:8000"
