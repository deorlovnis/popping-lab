# Testing Contract Claims

Contract claims are tested by executing code and verifying behavior.

## Methodology

### 1. Set Up Test Environment

- Identify target (endpoint, function, CLI)
- Gather credentials/config if needed
- Ensure test isolation (don't pollute production)

### 2. Design Test Cases

For each claim, create:
- **Happy path** — Normal input, expected output
- **Edge cases** — Boundaries, empty, max
- **Error cases** — Invalid input, unauthorized

### 3. Execute Tests

Run actual code. Options:

**HTTP Endpoints:**
```python
import requests

response = requests.post(
    "http://localhost:8000/login",
    json={"username": "test", "password": "wrong"}
)

print(f"Status: {response.status_code}")
print(f"Body: {response.json()}")
```

**Functions:**
```python
from mymodule import validate_input

try:
    result = validate_input(None)
    print(f"Result: {result}")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")
```

**CLI:**
```python
import subprocess

result = subprocess.run(
    ["./mycli", "--verbose", "process"],
    capture_output=True,
    text=True
)

print(f"Exit code: {result.returncode}")
print(f"Stdout: {result.stdout}")
print(f"Stderr: {result.stderr}")
```

### 4. Capture Observations

Record:
- Exact output (status codes, responses, exceptions)
- Timing if relevant
- Any unexpected behavior

### 5. Compare to Kill Criteria

For each criterion:
- Is it met? Document evidence.
- Not met? Claim survives this test.

## Output Format

```yaml
test:
  method: "HTTP POST to /login with invalid credentials"
  code: |
    import requests
    response = requests.post(url, json=payload)
    print(response.status_code, response.json())
observations:
  raw: |
    Status: 401
    Body: {"error": "Invalid credentials"}
  unexpected: "None"
verdict: SURVIVED
reasoning: "Criterion was 401 response - received 401. Claim holds."
```

## Common Testing Patterns

### Assert Status Code
```python
assert response.status_code == 401, f"Expected 401, got {response.status_code}"
```

### Assert Response Structure
```python
body = response.json()
assert "error" in body, "Missing error field"
assert isinstance(body["error"], str), "Error should be string"
```

### Assert Exception Type
```python
import pytest

with pytest.raises(ValueError):
    validate_input(None)
```

## Tips

1. **Test real code** — Mocks can lie
2. **Capture raw output** — Don't summarize prematurely
3. **Test boundaries** — 0, 1, max, max+1
4. **Test auth** — Both valid and invalid
5. **Isolate tests** — Don't depend on state from other tests
