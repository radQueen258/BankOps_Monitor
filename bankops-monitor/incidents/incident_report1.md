# Incident INC-001 — Banking API Database Connection Failure

## Root Cause
PostgreSQL database container was stopped, causing application database connections to fail.

## Resolution
Restored the PostgreSQL container and verified the /health endpoint returned HTTP 200.

## Evidence and Observations
Not yet recorded.