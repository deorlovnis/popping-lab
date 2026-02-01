# Testing Equality Claims

Equality claims are tested by comparing actual results to expected values.

Kill target: **Find input where X ≠ Y**

## Methodology

### 1. Set Up Test Environment

- Identify target (endpoint, function, CLI)
- Gather credentials/config if needed
- Ensure test isolation

### 2. Design Test Cases

For each equality claim, test:
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
from mymodule import add

result = add(2, 2)
expected = 4
print(f"Result: {result}, Expected: {expected}, Equal: {result == expected}")
```

### 4. Capture Observations

Record:
- Exact output (status codes, responses, return values)
- Timing if relevant
- Any X ≠ Y findings

### 5. Compare to Kill Criteria

For each test case:
- Does X equal Y? → SURVIVED this test
- Does X ≠ Y? → KILLED

## Output Format

```yaml
test:
  method: "Compared add(2,2) to expected value 4"
  code: |
    result = add(2, 2)
    expected = 4
    assert result == expected
observations:
  raw: |
    Result: 4
    Expected: 4
    Equal: True
  unexpected: "None"
verdict: SURVIVED
reasoning: "X = Y for all test cases. No inequality found."
```

## Common Equality Tests

### Assert Exact Match
```python
assert actual == expected, f"Expected {expected}, got {actual}"
```

### Assert Structure Match
```python
assert response.json() == {"status": "ok", "id": 123}
```

### Assert Approximate (floats)
```python
import math
assert math.isclose(actual, expected, rel_tol=1e-9)
```

## Tips

1. **Test real code** — Mocks can lie
2. **Use property testing** — hypothesis finds edge cases
3. **Check type equality** — 1 vs "1" matters
4. **Consider NaN** — NaN ≠ NaN in IEEE floats
