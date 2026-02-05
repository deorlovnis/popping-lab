# Invariant Claim Refinement → Modal Truth

Invariant claims test that property P always holds. In Veritas, these become **Modal** truths.

**Veritas Type:** `Modal`
**Falsification Form:** ◇¬P (find state where ¬P)

## Characteristics

- Property must hold across ALL states/inputs
- Often about bounds, constraints, performance
- Requires searching for violations
- Single counterexample kills the claim

## Refinement Process

### 1. Identify the Invariant

What property P must always be true?

| Vague | Sharp |
|-------|-------|
| "Balance stays positive" | "balance >= 0 after any transaction" |
| "Caching helps" | "p95 latency < 100ms under normal load" |
| "Thread safe" | "No data races under concurrent access" |

### 2. Quantify the Bound

Be specific about:
- The measurement (what P measures)
- The threshold (what value must hold)
- The scope (when/where it must hold)
- The conditions (under what circumstances)

### 3. Define the Search Space

Where might violations occur?
- State transitions
- Boundary conditions
- Concurrent operations
- Resource exhaustion
- Time-dependent behavior

### 4. Set Falsification Form

For Modal: **◇¬P** (possibility of violation)

Expressed as: ∃state: ¬P(state)

Examples:
- "◇(balance < 0) — find state where balance goes negative"
- "◇(latency > 100ms) — find state exceeding bound"
- "◇(data_race) — find concurrent state with race"

## Veritas Output Template

```python
from veritas import Modal, sym

# Define the state variable
balance = sym("balance")

# Create Modal truth
truth = Modal(
    statement="balance >= 0 after any transaction",
    invariant=balance >= 0,
    state_var="balance",
)

# Performance bound
latency = sym("latency")
truth = Modal(
    statement="p95 latency < 100ms",
    invariant=latency < 100,
    state_var="latency",
)
```

## Testing Strategies

| Strategy | Method | Veritas Pattern |
|----------|--------|-----------------|
| Fuzz testing | Random inputs seeking ¬P | hypothesis + Modal |
| Boundary testing | Test at limits | pytest + Modal |
| SMT solving | Prove no ¬P exists | z3 + SymPy |
| Load testing | Stress test bounds | locust + Modal |

## Common Mistakes

1. **No quantification** — "fast" vs "< 100ms"
2. **Missing conditions** — Under what load?
3. **Single test** — Invariants need exhaustive search
4. **Wrong scope** — Does it hold always or usually?
5. **Correlation ≠ causation** — Is the bound causal?
