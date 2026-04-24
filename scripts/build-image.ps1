Param(
  [string]$Tag = "local"
)
$ErrorActionPreference = "Stop"

docker build -t "platform-backend:$Tag" app/backend
