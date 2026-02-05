# Ordering Claim Refinement → Analytic Truth

Ordering claims test that X ≤ Y relationship holds. In Veritas, these become **Analytic** truths with an ordering predicate.

**Veritas Type:** `Analytic`
**Falsification Form:** ∃x,y: order(x,y) violated

## Characteristics

- Comparison relationship between elements
- Order must be preserved/respected
- May involve transitivity (if A < B and B < C, then A < C)
- Single order violation kills the claim

## Refinement Process

### 1. Identify the Ordering

What ordering relationship is being claimed?

| Vague | Sharp |
|-------|-------|
| "Results are sorted" | "Search results sorted by relevance score descending" |
| "FIFO queue" | "Dequeue order matches enqueue order" |
| "Priority works" | "Higher priority tasks execute before lower" |

### 2. Define the Comparison

Be explicit about:
- What property determines order
- Direction (ascending, descending)
- Tie-breaking rules
- Stability requirements

### 3. Identify Test Scenarios

Where might order be violated?
- After insertions
- After deletions
- Under concurrent access
- At boundaries (empty, single, full)
- With equal elements (ties)

### 4. Set Falsification Form

For Analytic (ordering): **∃i: seq[i] > seq[i+1]** (for ascending)

Examples:
- "∃i: results[i].score < results[i+1].score for descending"
- "∃dequeue: dequeue order ≠ enqueue order"
- "∃tasks: lower priority executed before higher"

## Veritas Output Template

```python
from veritas import Analytic

# Sort verification
truth = Analytic(
    statement="list is sorted ascending",
    lhs="is_sorted",
    rhs=True,
)

# FIFO property
truth = Analytic(
    statement="dequeue order matches enqueue order",
    lhs="order_preserved",
    rhs=True,
)

# Priority ordering
truth = Analytic(
    statement="high priority tasks complete before low priority",
    lhs="priority_respected",
    rhs=True,
)

# Stability (equal elements keep original order)
truth = Analytic(
    statement="sort is stable for equal keys",
    lhs="is_stable",
    rhs=True,
)
```

## Testing Strategies

| Strategy | Method | Veritas Pattern |
|----------|--------|-----------------|
| Pairwise comparison | Check adjacent pairs | `claim(Analytic(...))` |
| Transitivity checks | Verify A<B, B<C → A<C | hypothesis + Analytic |
| Stability tests | Equal elements preserve order | pytest + Analytic |
| Concurrent tests | Order under race conditions | threading + Analytic |

## Common Mistakes

1. **Undefined comparison** — How exactly is order determined?
2. **Ignoring ties** — What happens with equal elements?
3. **Missing transitivity** — Order must be consistent
4. **Stability confusion** — Does insertion order matter for equals?
