# Helm Release Process

## Deploy dev

```bash
make helm-deploy-dev
```

## Deploy staging

```bash
make helm-deploy-staging
```

## Deploy prod

```bash
make helm-deploy-prod
```

## Process model

1. Render and validate chart with environment values.
2. Upgrade/install release per namespace.
3. Confirm rollout health and service accessibility.
4. Promote by tag and manual approval for prod.
