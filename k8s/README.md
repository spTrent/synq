# Application: Synq

This directory contains the application deployment manifests using Kustomize and Helm.

## Directory Structure

- `kustomization/`: Kustomize manifests.
  - `base/`: Shared resources (backend, frontend, ingress, etc.).
  - `overlays/`: Environment-specific configurations (dev, prod).
- `helm/`: Helm chart for the application.

## Prerequisites

- Infrastructure (PostgreSQL, Redis) must be deployed first. See `infra/postgres/README.md`.

## Deployment with Kustomize

1. Deploy the development environment:
   ```bash
   kubectl apply -k k8s/kustomization/overlays/dev
   ```

2. Deploy the production environment:
   ```bash
   kubectl apply -k k8s/kustomization/overlays/prod
   ```

## Deployment with Helm

1. Install the chart for development:
   ```bash
   helm install synq-dev ./k8s/helm/synq -f ./k8s/helm/synq/values-dev.yaml
   ```

2. Install the chart for production:
   ```bash
   helm install synq-prod ./k8s/helm/synq -f ./k8s/helm/synq/values-prod.yaml
   ```

## Health Checks

- Backend: `GET /api/v1/auth/registry` (returns 405 if alive)
- Metrics: `GET /metrics`
- Frontend: `GET /`
