# BankOps Monitor

A local training lab for application support: a fictional banking transactions API, PostgreSQL, health checks and Prometheus-compatible metrics.

## Start

Install Docker Desktop with Docker Compose. Open a terminal in this folder:

```bash
docker compose up --build -d
docker compose ps
```

Open http://localhost:8000/docs and test GET /health, POST /transactions, and GET /transactions.

Sample transaction:

```json
{"account_id":"DEMO-001","amount":150.00,"transaction_type":"deposit"}
```

Metrics: http://localhost:8000/metrics

## Incident lab: database outage

```bash
docker compose stop db
```

Open http://localhost:8000/health. Expect HTTP 503. Investigate:

```bash
docker compose ps
docker compose logs --tail=30 api
docker compose logs --tail=30 db
```

Recover:

```bash
docker compose start db
```

Retry /health (recovery may take a few seconds).

## Stop

```bash
docker compose down
```

Do not use `docker compose down -v` unless you want to remove the database data volume.

## Safety and scope

All accounts and transactions are fictional. The API has no authentication and is for local use only, not for deployment or actual banking activity. The credentials are development-only.
