# Testing Invariant Claims → Modal Verification

Invariant claims are tested using **Modal** truths in Veritas.

**Kill target:** ◇¬P (find state where property P is violated)

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

### 3. Execute with Veritas

```python
from veritas import claim, Modal, sym, Verdict

# Define the invariant
balance = sym("balance")
truth = Modal(
    statement="balance >= 0 after any transaction",
    invariant=balance >= 0,
    state_var="balance",
)

# Test by searching for violations
with claim(truth) as c:
    # Simulate transactions
    test_balance = simulate_transactions()
    c.bind(balance=test_balance, state=test_balance)

# Veritas checks if violation was found
print(c.result.verdict)
```

### 4. Property-Based Testing

```python
from veritas import Modal, Verifier, Evidence, sym
from hypothesis import given, strategies as st

balance = sym("balance")
truth = Modal(
    statement="balance >= 0",
    invariant=balance >= 0,
)

@given(st.integers(), st.integers())
def test_balance_invariant(deposit, withdraw):
    account = Account(deposit)
    account.withdraw(withdraw)

    evidence = Evidence(bindings={
        "balance": account.balance,
        "state": account.balance,
    })

    result = Verifier().verify(truth, evidence)
    assert result.verdict != Verdict.KILLED, f"Violated at balance={account.balance}"
```

### 5. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Found state where ¬P | KILLED |
| Searched thoroughly, no violation | SURVIVED |
| Incomplete search | UNCERTAIN |

## Testing Patterns

### Performance Bound

```python
from veritas import claim, Modal, sym
import time

latency = sym("latency")
truth = Modal(
    statement="response time < 100ms",
    invariant=latency < 100,
)

with claim(truth) as c:
    start = time.perf_counter()
    result = operation()
    elapsed_ms = (time.perf_counter() - start) * 1000
    c.bind(latency=elapsed_ms, state=elapsed_ms)

if c.result.verdict == Verdict.KILLED:
    print(f"Performance bound violated: {elapsed_ms}ms")
```

### State Consistency

```python
from veritas import claim, Modal, sym

# Invariant: total == sum(items)
total = sym("total")
items_sum = sym("items_sum")

truth = Modal(
    statement="total equals sum of items",
    invariant=total == items_sum,
)

with claim(truth) as c:
    state = get_system_state()
    c.bind(
        total=state.total,
        items_sum=sum(state.items),
        state=state,
    )
```

### Boundary Testing

```python
from veritas import Modal, Evidence, Verifier, sym

x = sym("x")
truth = Modal(
    statement="result always positive",
    invariant=x > 0,
)

test_cases = [0, 1, -1, float('inf'), float('-inf'), None]
verifier = Verifier()

for case in test_cases:
    if case is not None:
        evidence = Evidence(bindings={"x": case, "state": case})
        result = verifier.verify(truth, evidence)
        if result.is_killed():
            print(f"Invariant violated at x={case}")
            break
```

## Tips

1. **Use hypothesis** — It finds edge cases automatically
2. **Test boundaries** — Violations often at limits
3. **Test transitions** — Check invariant after each state change
4. **Document coverage** — What % of state space was searched?
