# Incident Runbook

## 1) Pipeline failure

- Inspect failed job logs in GitLab.
- Reproduce locally with `make test` or `make security`.
- Patch, rerun pipeline, document root cause and prevention.

## 2) Runner offline

- Check runner container: `docker logs local-gitlab-runner`.
- Restart runner service.
- Re-register token if invalid/rotated.

## 3) Kubernetes rollout failure

- `kubectl -n <ns> rollout status deploy/<name>`.
- `kubectl -n <ns> describe deploy/<name>`.
- Roll back Helm release if needed: `helm rollback`.

## 4) Pod CrashLoopBackOff

- `kubectl -n <ns> logs <pod> --previous`.
- Validate env/config/secret references.
- Fix image/config and redeploy.

## 5) Payment webhook failure

- Verify webhook signature header and payload.
- Check backend logs for 401/400 patterns.
- Replay event with valid test signature.

## 6) Elevated latency

- Check Grafana latency and request-rate panels.
- Inspect pod CPU/memory and HPA state.
- Scale replicas or mitigate noisy dependency behavior.

## 7) Failed security scan

- Identify failing control (`bandit`, `gitleaks`, `trivy`, audits).
- Block release until fixed or risk-accepted with documented approval.

## 8) Suspected secret exposure

- Rotate impacted credential immediately.
- Purge history if required (`git filter-repo` process in secure mirror).
- Add/update secret scan rules and post-incident review.
