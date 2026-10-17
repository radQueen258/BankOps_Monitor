# INC-001 — Banking Transaction Service Unavailable

**Environment:** BankOps Monitor — Local Development  
**Severity:** SEV 2 (simulated)  
**Status:** Resolved (complete after verifying recovery)

## 1. Incident Description
The banking API was unable to access the PostgreSQL database, causing transaction retrieval and creation requests to fail.

## 2. Detection
The issue was detected through the `/health` endpoint, which returned HTTP 503 — Service Unavailable.

## 3. Investigation
- Inspected Docker containers using `docker compose ps -a`.
- Checked API logs using `docker compose logs --tail=50 api`.
- Checked PostgreSQL logs using `docker compose logs --tail=30 db`.
- Identified that the PostgreSQL database container was stopped.

## 4. Root Cause
The PostgreSQL container had been intentionally stopped to simulate a database outage. This made database connections unavailable to the API.

## 5. Resolution
Restarted the database container using `docker compose start db`.

## 6. Verification
- Confirmed the database container returned to a healthy state.
- Confirmed `/health` returned HTTP 200.
- Confirmed the `/transactions` endpoint could retrieve records.

## 7. Preventive Measures
- Configure monitoring to detect database connectivity failures.
- Set up alerts for API errors and service unavailability.
- Document database recovery procedures in a support runbook.

## 8. Lessons Learned
An API container can remain running even when its database is unavailable. Application-level health checks, service logs, and database checks are necessary to identify the underlying problem.