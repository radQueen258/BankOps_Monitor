# Incident INC-001 — Banking API Database Connection Failure


**Project:** BankOps Monitor  
**Environment:** Local Docker Compose  
**Type:** Simulated application incident  
**Status:** Resolved
## Root Cause


## Incident summary

A PostgreSQL database outage was simulated to test application health monitoring, incident detection, troubleshooting, and service recovery.

## Detection

The Python health monitoring script detected a change in application status from `UP` to `DOWN`, returning HTTP 503.

## Resolution
Restored the PostgreSQL container and verified the /health endpoint returned HTTP 200.

## Verification

The automated health-monitoring script detected recovery and returned HTTP 200.

Subsequent Bash diagnostics confirmed that the API was healthy, PostgreSQL was running, and service logs were accessible.

## Lessons learned

- Running application containers do not guarantee healthy dependencies.
- HTTP health checks can help detect database connectivity problems.
- Automated scripts support faster incident detection.
- Docker logs provide useful diagnostic evidence.
- Recovery should be verified after services are restarted.
