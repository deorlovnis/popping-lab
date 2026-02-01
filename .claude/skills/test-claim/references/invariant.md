# Testing Invariant Claims

Invariant claims require searching for states where the property is violated.

Kill target: **Find state where ¬P**

## Methodology

### 1. Identify the Invariant

What property P must always hold?
- Balance >= 0
- Response time < 100ms
- No null pointers

### 2. Design the Search

Where might violations hide?
- Boundary conditions
- State transitions
- Concurrent operations
- Resource limits
- Time-dependent behavior

### 3. Execute Search Strategies

**Property-based testing (recommended):**
```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_balance_never_negative(deposit, withdraw):
    account = Account(deposit)
    account.withdraw(withdraw)
    assert account.balance >= 0  # Kill if violated
```

**Fuzz testing:**
```python
import random

for _ in range(10000):
    inputs = [random.randint(-1000, 1000) for _ in range(10)]
    state = process(inputs)
    assert invariant_holds(state), f"Violated with {inputs}"
```

**Boundary testing:**
```python
# Test at limits
test_cases = [0, 1, -1, MAX_INT, MIN_INT, None]
for case in test_cases:
    result = process(case)
    assert invariant_holds(result)
```

### 4. Capture Observations

Record:
- Any violation found (this kills the claim)
- Search coverage (how much state space explored)
- Near-violations (close to boundary)

### 5. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Found state where ¬P | KILLED |
| Searched thoroughly, no violation | SURVIVED |
| Incomplete search | UNCERTAIN |

## Output Format

```yaml
test:
  method: "Property-based testing with 10,000 random inputs"
  code: |
    @given(st.integers())
    def test_invariant(x):
        result = process(x)
        assert result >= 0
observations:
  raw: |
    Ran 10,000 examples
    Found violation at x = -5: result = -3
  unexpected: "Negative input not handled"
verdict: KILLED
reasoning: "Invariant 'result >= 0' violated when x = -5"
```

## Invariant Testing Patterns

### Always Non-negative
```python
assert value >= 0, f"Negative value: {value}"
```

### Performance Bound
```python
import time
start = time.perf_counter()
result = operation()
elapsed = time.perf_counter() - start
assert elapsed < 0.1, f"Took {elapsed}s, exceeds 100ms bound"
```

### State Consistency
```python
def check_invariant(state):
    assert state.total == sum(state.items)
    assert len(state.items) <= state.max_size
```

## Tips

1. **Use hypothesis** — It finds edge cases automatically
2. **Test boundaries** — Violations often at limits
3. **Test transitions** — Check invariant after each state change
4. **Document coverage** — What % of state space was searched?
