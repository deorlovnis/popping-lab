# Equality Claim Refinement → Analytic Truth

Equality claims test that X equals Y. In Veritas, these become **Analytic** truths.

**Veritas Type:** `Analytic`
**Falsification Form:** ∃x: f(x) ≠ expected

## Also Covers

- **Membership:** X ∈ S → Analytic with set predicate
- **Ordering:** X ≤ Y → Analytic with comparison predicate

## Characteristics

- Specific input → expected output
- Deterministic (same input = same result)
- Direct comparison possible
- Single counterexample kills the claim

## Refinement Process

### 1. Identify the Equality

What two things are being compared?

| Vague | Sharp |
|-------|-------|
| "Login should work" | "POST /login with valid credentials returns 200" |
| "Parser works" | "parse('2024-01-01') returns Date(2024, 1, 1)" |
| "Math is correct" | "add(2, 2) equals 4" |

### 2. Specify Both Sides

Be explicit about:
- Left side (lhs): variable name for actual result
- Right side (rhs): expected value
- Comparison semantics (exact match, approximate, structural)

### 3. Define Test Inputs

What inputs will be tested?
- Happy path inputs
- Edge cases (empty, null, max)
- Boundary values

### 4. Set Falsification Form

For Analytic: **∃x: lhs ≠ rhs**

Examples:
- "∃x: add(x, 2) ≠ x + 2"
- "∃x: status_code ≠ 200"
- "∃input: parse(input) ≠ expected"

## Veritas Output Template

```python
from veritas import Analytic

# Simple equality
truth = Analytic(
    statement="add(2, 2) equals 4",
    lhs="result",  # variable name for actual
    rhs=4,         # expected value
)

# Membership as equality
truth = Analytic(
    statement="email is valid RFC 5322",
    lhs="is_valid",
    rhs=True,
)

# Ordering as equality
truth = Analytic(
    statement="list is sorted ascending",
    lhs="is_sorted",
    rhs=True,
)
```

## Testing Strategies

| Strategy | Method | Veritas Pattern |
|----------|--------|-----------------|
| Unit test | Assert X == Y | `claim(Analytic(...))` |
| Property test | For all inputs, X == Y | hypothesis + Analytic |
| Formal proof | Prove X = Y | SymPy simplification |

## Common Mistakes

1. **Vague expected value** — "returns success" vs "returns {'ok': true}"
2. **Missing edge cases** — What about empty input?
3. **Wrong comparison** — Reference equality vs value equality
4. **Floating point** — Use approximate equality for floats
