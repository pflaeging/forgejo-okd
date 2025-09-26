# Instance Template

This template is for deploying Forgejo on a gubernat or openshift cluster.

Depending on which option you choose, use the correct storage classes in `forgejo-config.yaml`, `valkey-config.yaml` and `postgres-config.yaml`, and choose between ingress (for gubernat) or route (for openshift).

## Installation

`kubectl kustomize . --enable-helm --load-restrictor=LoadRestrictionsNone | kubectl apply -f -`

## CloudNativePG operator install

### Operator on plain kubernetes

As cluster admin:

```shell
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm upgrade --install cnpg \
  --namespace cnpg-system \
  --create-namespace \
  cnpg/cloudnative-pg
```

Operator runs in namespace: `cnpg-system`.

PostgreSQL clusters are rolled out with CRD's: `clusters.postgresql.cnpg.io`

### Operator on OpenShift / OKD

As cluster admin: `oc apply -f subscription.yaml` .

This installs the operator via OLM in OpenShift / OKD
