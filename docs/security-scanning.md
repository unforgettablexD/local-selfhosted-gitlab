# Security Scanning

## Included controls

- `pip-audit` for Python dependencies.
- `npm audit` for Node dependencies.
- `bandit` SAST for backend code.
- `gitleaks` secret scanning.
- `trivy` container vulnerability + secret scanning.
- `api_exposure_check.py` to ensure admin routes require auth.

## Secret handling

- Use `.example` secret manifests only.
- Store real credentials in CI/CD variables or secret managers (not in git).
- Demo includes fake webhook signature and fake tokens only.

## RBAC and org isolation

- Non-admin users are restricted to their own `org_id`.
- Admin endpoints require explicit admin role checks.
- Cross-org request attempts return `403`.
