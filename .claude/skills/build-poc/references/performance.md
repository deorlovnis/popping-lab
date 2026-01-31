# Performance POC Patterns

For claims about speed, latency, throughput, or resource usage.

## Basic Benchmark

```python
#!/usr/bin/env python3
"""
POC: Benchmark [operation]

Run: python main.py
"""

import statistics
import time
from typing import Callable


def benchmark(func: Callable, n_iterations: int = 100, warmup: int = 10) -> dict:
    """Run function multiple times and collect timing stats."""

    # Warmup runs (not counted)
    for _ in range(warmup):
        func()

    # Timed runs
    times = []
    for _ in range(n_iterations):
        start = time.perf_counter()
        func()
        elapsed = time.perf_counter() - start
        times.append(elapsed * 1000)  # Convert to ms

    return {
        "n": n_iterations,
        "mean_ms": round(statistics.mean(times), 3),
        "median_ms": round(statistics.median(times), 3),
        "stdev_ms": round(statistics.stdev(times), 3) if len(times) > 1 else 0,
        "min_ms": round(min(times), 3),
        "max_ms": round(max(times), 3),
        "p95_ms": round(sorted(times)[int(n_iterations * 0.95)], 3),
        "p99_ms": round(sorted(times)[int(n_iterations * 0.99)], 3),
    }


def operation_to_test():
    """The operation being benchmarked."""
    # Replace with actual code
    time.sleep(0.01)  # Simulate work


def main():
    print("Benchmarking: [operation]")
    print("-" * 40)

    results = benchmark(operation_to_test, n_iterations=100)

    for key, value in results.items():
        print(f"{key}: {value}")

    # Evaluate against criteria
    threshold = 50  # ms
    success = results["p95_ms"] < threshold
    print(f"\nThreshold: p95 < {threshold}ms")
    print(f"Verdict: {'PASS' if success else 'FAIL'}")


if __name__ == '__main__':
    main()
```

## Comparing Two Approaches

```python
#!/usr/bin/env python3
"""Compare performance of two implementations."""

import statistics
import time


def approach_a():
    """First approach."""
    pass


def approach_b():
    """Second approach."""
    pass


def compare(func_a, func_b, n_iterations=100):
    """Compare two functions."""

    def measure(func):
        times = []
        for _ in range(n_iterations):
            start = time.perf_counter()
            func()
            times.append(time.perf_counter() - start)
        return times

    times_a = measure(func_a)
    times_b = measure(func_b)

    mean_a = statistics.mean(times_a) * 1000
    mean_b = statistics.mean(times_b) * 1000

    improvement = ((mean_a - mean_b) / mean_a) * 100 if mean_a > 0 else 0

    return {
        "approach_a_mean_ms": round(mean_a, 3),
        "approach_b_mean_ms": round(mean_b, 3),
        "improvement_pct": round(improvement, 1),
        "faster": "B" if mean_b < mean_a else "A",
    }


def main():
    results = compare(approach_a, approach_b)

    print(f"Approach A: {results['approach_a_mean_ms']}ms")
    print(f"Approach B: {results['approach_b_mean_ms']}ms")
    print(f"Improvement: {results['improvement_pct']}%")
    print(f"Winner: Approach {results['faster']}")


if __name__ == '__main__':
    main()
```

## Memory Profiling

```python
#!/usr/bin/env python3
"""Profile memory usage."""

import tracemalloc


def profile_memory(func):
    """Measure memory usage of a function."""
    tracemalloc.start()

    func()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "current_mb": round(current / 1024 / 1024, 2),
        "peak_mb": round(peak / 1024 / 1024, 2),
    }


def operation_to_test():
    """The operation being profiled."""
    data = [i ** 2 for i in range(1000000)]
    return data


def main():
    print("Memory profiling: [operation]")

    results = profile_memory(operation_to_test)

    print(f"Current memory: {results['current_mb']} MB")
    print(f"Peak memory: {results['peak_mb']} MB")


if __name__ == '__main__':
    main()
```

## Load Testing (with locust)

```python
#!/usr/bin/env python3
"""
Load test for API endpoint.

Run: locust -f main.py --host=http://localhost:8000
"""

from locust import HttpUser, task, between


class APIUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def test_endpoint(self):
        self.client.get("/api/endpoint")

    @task(3)  # 3x more likely
    def test_main_endpoint(self):
        self.client.post("/api/main", json={"key": "value"})
```

## Quick HTTP Benchmark

```python
#!/usr/bin/env python3
"""Quick HTTP endpoint benchmark."""

import statistics
import time

import requests

URL = "http://localhost:8000/api/endpoint"
N_REQUESTS = 100


def main():
    times = []

    for i in range(N_REQUESTS):
        start = time.perf_counter()
        response = requests.get(URL)
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)

        if response.status_code != 200:
            print(f"Request {i} failed: {response.status_code}")

    print(f"Requests: {N_REQUESTS}")
    print(f"Mean: {statistics.mean(times):.1f}ms")
    print(f"Median: {statistics.median(times):.1f}ms")
    print(f"P95: {sorted(times)[int(N_REQUESTS * 0.95)]:.1f}ms")
    print(f"Min: {min(times):.1f}ms")
    print(f"Max: {max(times):.1f}ms")


if __name__ == '__main__':
    main()
```

## Tips

1. **Warmup** — First runs are often slower (JIT, caching)
2. **Many iterations** — Reduce noise
3. **Use perf_counter** — Higher resolution than time.time()
4. **Control variables** — Same machine, same data, same conditions
5. **Report percentiles** — P95/P99 often matter more than mean
6. **Document environment** — CPU, memory, OS, Python version
