
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

API_URL = "http://localhost:8000/health"
LOG_FILE = Path(__file__).parent / "health_checks.jsonl"


def check_health():
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        with urlopen(API_URL, timeout=5) as response:
            http_status = response.status
            data = json.load(response)

        healthy = (
            http_status == 200
            and data.get("status") == "healthy"
            and data.get("database") == "connected"
        )

        result = {
            "timestamp": timestamp,
            "status": "UP" if healthy else "DOWN",
            "http_status": http_status
        }

    except HTTPError as error:
        result = {
            "timestamp": timestamp,
            "status": "DOWN",
            "http_status": error.code,
            "error": str(error)
        }

    except (URLError, TimeoutError, OSError, ValueError) as error:
        result = {
            "timestamp": timestamp,
            "status": "DOWN",
            "http_status": None,
            "error": str(error)
        }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(result) + "\n")

    print(result, flush=True)


if __name__ == "__main__":
    print("BankOps Health Monitor started...")

    try:
        while True:
            check_health()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
