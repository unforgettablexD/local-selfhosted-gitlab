# CI/CD Pipeline Design

Pipeline file: `.gitlab-ci.yml`

## Stages

- `lint`: static quality checks (`ruff_lint`)
- `test`: backend and frontend tests
- `security`: dependency scans, SAST, secret scan, container scan, custom API exposure check
- `build`: docker image build
- `package`: optional docker push
- `deploy_staging`: automatic Helm deploy
- `deploy_prod`: manual approval Helm deploy

## Required Variables

- `CI_REGISTRY_IMAGE`
- `KUBE_CONTEXT`
- `HELM_RELEASE_NAME`
- `STAGING_NAMESPACE`
- `PROD_NAMESPACE`
- `KUBECONFIG_B64` (base64-encoded kubeconfig)

## Why this is production-style

- Shifts security left with fail-fast security gates.
- Splits build/package/deploy concerns.
- Uses manual approval before prod release.
- Uses environment-specific Helm values for drift control.
