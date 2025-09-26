# CloudNativePG with operator install

## Operator (for kubernetes)

```shell
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm upgrade --install cnpg \
  --namespace cnpg-system \
  --create-namespace \
  cnpg/cloudnative-pg
```

Operator runs in namespace: `cnpg-system`.

PostgreSQL clusters are rolled out with CRD's: `clusters.postgresql.cnpg.io`
