Param(
  [string]$Mode = "all"
)
$ErrorActionPreference = "Stop"

Push-Location "app/backend"
python -m pip install -r requirements.txt | Out-Null

if ($Mode -eq "security") {
  python -m ruff check src tests
  python -m bandit -c ../../security/bandit.yaml -r src
  python -m pip_audit -r requirements.txt
} else {
  python -m ruff check src tests
  python -m pytest -q
}
Pop-Location

if ($Mode -ne "security") {
  Push-Location "app/frontend"
  npm test
  Pop-Location
}

if ($Mode -eq "security") {
  python security/api_exposure_check.py
}
