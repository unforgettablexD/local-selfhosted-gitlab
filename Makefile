.PHONY: prereqs gitlab-up gitlab-down runner-register app-up app-down test security kind-create kind-destroy k8s-deploy helm-deploy-dev helm-deploy-staging helm-deploy-prod observability-up dashboard-up platform-up clean

prereqs:
	powershell -ExecutionPolicy Bypass -File scripts/check-prereqs.ps1

gitlab-up:
	docker compose -f gitlab/docker-compose.gitlab.yml up -d

gitlab-down:
	docker compose -f gitlab/docker-compose.gitlab.yml down

runner-register:
	powershell -ExecutionPolicy Bypass -File gitlab/runner/register-runner.ps1

app-up:
	docker compose up -d --build

app-down:
	docker compose down

test:
	powershell -ExecutionPolicy Bypass -File scripts/test-all.ps1

security:
	powershell -ExecutionPolicy Bypass -File scripts/test-all.ps1 security

kind-create:
	powershell -ExecutionPolicy Bypass -File scripts/create-kind-cluster.ps1

kind-destroy:
	powershell -ExecutionPolicy Bypass -File scripts/destroy-kind-cluster.ps1

k8s-deploy:
	powershell -ExecutionPolicy Bypass -File scripts/deploy-k8s.ps1

helm-deploy-dev:
	powershell -ExecutionPolicy Bypass -File scripts/deploy-helm.ps1 dev

helm-deploy-staging:
	powershell -ExecutionPolicy Bypass -File scripts/deploy-helm.ps1 staging

helm-deploy-prod:
	powershell -ExecutionPolicy Bypass -File scripts/deploy-helm.ps1 prod

observability-up:
	docker compose -f observability/docker-compose.observability.yml up -d

dashboard-up:
	npm --prefix app/frontend start

platform-up:
	powershell -ExecutionPolicy Bypass -File scripts/platform-up.ps1

clean:
	powershell -ExecutionPolicy Bypass -File scripts/clean-local.ps1
