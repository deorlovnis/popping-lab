# API POC Patterns

For claims involving API calls, services, or backend logic.

## Basic Structure

```python
#!/usr/bin/env python3
"""
POC: <claim statement>

Run: python main.py
"""

import json
import time
from typing import Any

import requests  # or httpx, aiohttp

BASE_URL = "https://api.example.com"


def test_claim() -> dict[str, Any]:
    """Execute the test and return observations."""
    start = time.time()

    # Make the API call
    response = requests.post(
        f"{BASE_URL}/endpoint",
        json={"key": "value"},
        headers={"Authorization": "Bearer TOKEN"}
    )

    elapsed = time.time() - start

    return {
        "status_code": response.status_code,
        "body": response.json() if response.ok else response.text,
        "elapsed_ms": round(elapsed * 1000, 2),
    }


def main():
    print("Testing: <claim>")
    print("-" * 40)

    result = test_claim()

    print(f"Status: {result['status_code']}")
    print(f"Time: {result['elapsed_ms']}ms")
    print(f"Response: {json.dumps(result['body'], indent=2)}")

    # Evaluate against criteria
    success = result['status_code'] == 200
    print(f"\nVerdict: {'PASS' if success else 'FAIL'}")


if __name__ == '__main__':
    main()
```

## With Authentication

```python
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    print("Error: Set API_KEY environment variable")
    exit(1)

headers = {"Authorization": f"Bearer {API_KEY}"}
```

## With Retries

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def call_api():
    return requests.get(url)
```

## Measuring Latency

```python
import statistics
import time

def benchmark(n_requests: int = 10) -> dict:
    """Run multiple requests and collect timing stats."""
    times = []

    for _ in range(n_requests):
        start = time.time()
        requests.get(url)
        times.append(time.time() - start)

    return {
        "mean_ms": round(statistics.mean(times) * 1000, 2),
        "p50_ms": round(statistics.median(times) * 1000, 2),
        "p95_ms": round(sorted(times)[int(n_requests * 0.95)] * 1000, 2),
        "min_ms": round(min(times) * 1000, 2),
        "max_ms": round(max(times) * 1000, 2),
    }
```

## requirements.txt

```
requests>=2.28.0
# or for async:
# httpx>=0.24.0
# aiohttp>=3.8.0
```

## Tips

1. **Use environment variables** for secrets
2. **Add timing** to all calls
3. **Print raw responses** for debugging
4. **Handle errors gracefully** but visibly
5. **Keep it single-file** when possible
