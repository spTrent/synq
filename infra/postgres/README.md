# Infrastructure: PostgreSQL

This directory contains the PostgreSQL deployment manifests using Kustomize.

## Contract for Application

The application should use the following environment variables (or equivalent `DATABASE_URL`) to connect to the database:

| Variable | Description | Default (Dev) |
| --- | --- | --- |
| `DB_HOST` | Database service hostname | `dev-postgres` |
| `DB_PORT` | Database service port | `5432` |
| `DB_USER` | Database username | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` |
| `DB_NAME` | Database name | `synq` |

**DATABASE_URL Pattern:** `postgresql+psycopg2://<user>:<password>@<host>:<port>/<name>`

## Deployment Order

1. Deploy the infrastructure (this directory):
   ```bash
   kubectl apply -k infra/postgres/overlays/dev
   ```
2. Wait for PostgreSQL to be ready:
   ```bash
   kubectl wait --for=condition=ready pod -l app=postgres --timeout=60s
   ```
3. Deploy the application (see `k8s/README.md`).
