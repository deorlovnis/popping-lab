# Testing Equality Claims → Analytic Verification

Equality claims are tested using **Analytic** truths in Veritas.

**Kill target:** ∃x: X ≠ Y (find input where equality fails)

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

### 3. Execute with Veritas

```python
from veritas import claim, Analytic, Verdict

# Define the truth
truth = Analytic(
    statement="add(2, 2) equals 4",
    lhs="result",
    rhs=4,
)

# Test with claim() context manager
with claim(truth) as c:
    actual = 2 + 2
    c.bind(result=actual, x=actual)

# Veritas evaluates automatically
assert c.result.verdict == Verdict.SURVIVED
```

### 4. Capture Observations

Evidence is captured automatically via `c.bind()`:
- Exact output (return values, status codes)
- Timing if relevant
- Any unexpected behaviors

### 5. Let Veritas Verify

Veritas evaluates: Is `result ≠ 4`?
- If True → **KILLED** (found counterexample)
- If False → **SURVIVED** (equality holds)
- If Unknown → **UNCERTAIN**

## Testing Patterns

### HTTP Endpoints

```python
from veritas import claim, Analytic
import requests

truth = Analytic(
    statement="POST /login returns 200 for valid credentials",
    lhs="status_code",
    rhs=200,
)

with claim(truth) as c:
    response = requests.post(
        "http://localhost:8000/login",
        json={"username": "test", "password": "valid"}
    )
    c.bind(status_code=response.status_code, x=response.status_code)

print(c.result.verdict)  # SURVIVED or KILLED
```

### Functions

```python
from veritas import claim, Analytic

truth = Analytic(
    statement="parse('2024-01-01') returns expected date",
    lhs="result",
    rhs="2024-01-01",
)

with claim(truth) as c:
    from mymodule import parse
    result = str(parse("2024-01-01"))
    c.bind(result=result, x=result)
```

### Floating Point (use approximate comparison)

```python
from veritas import claim, Analytic
import math

truth = Analytic(
    statement="sqrt(2) ≈ 1.414",
    lhs="is_close",
    rhs=True,
)

with claim(truth) as c:
    result = math.sqrt(2)
    is_close = math.isclose(result, 1.414, rel_tol=1e-3)
    c.bind(is_close=is_close, x=is_close)
```

## Tips

1. **Test real code** — Mocks can lie
2. **Use property testing** — hypothesis finds edge cases
3. **Check type equality** — 1 vs "1" matters
4. **Consider NaN** — NaN ≠ NaN in IEEE floats
