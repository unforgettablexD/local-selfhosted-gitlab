Param()
$ErrorActionPreference = "Continue"

docker compose down -v
docker compose -f gitlab/docker-compose.gitlab.yml down -v
docker compose -f observability/docker-compose.observability.yml down -v
kind delete cluster --name devsecops-lab
