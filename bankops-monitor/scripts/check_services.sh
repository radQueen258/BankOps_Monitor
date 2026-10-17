
#!/usr/bin/env bash

set -uo pipefail

echo "=================================="
echo " BANKOPS - SERVICE DIAGNOSTICS"
echo "=================================="

failed=0

echo ""
echo "[1] Docker container status"

if docker compose ps -a; then
    echo "Docker inspection: OK"
else
    echo "ERROR: Unable to inspect containers"
    failed=1
fi

echo ""
echo "[2] Banking API health check"

http_code=$(curl -s -o /dev/null -w "%{http_code}" \
    --max-time 5 http://localhost:8000/health) || http_code="000"

if [ "$http_code" = "200" ]; then
    echo "SUCCESS: API healthy (HTTP 200)"
else
    echo "ALERT: API unhealthy (HTTP $http_code)"
    failed=1
fi

echo ""
echo "[3] Last 20 API log lines"

if ! docker compose logs --tail=20 api; then
    echo "ERROR: Could not retrieve API logs"
    failed=1
fi

echo ""
echo "[4] Last 20 database log lines"

if ! docker compose logs --tail=20 db; then
    echo "ERROR: Could not retrieve database logs"
    failed=1
fi

echo ""
echo "=================================="

if [ "$failed" -eq 0 ]; then
    echo "RESULT: PASS - Health checks succeeded"
else
    echo "RESULT: FAIL - Investigation required"
fi

exit "$failed"
