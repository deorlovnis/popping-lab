# Ordering Claim Refinement

Ordering claims test that X ≤ Y relationship holds — ranking, sorting, precedence.

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

### 4. Set Kill Criteria

What proves ordering is broken?

Kill template: **Find order violation (X > Y when X ≤ Y expected)**

Examples:
- "Dies if any result[i] > result[i+1] by relevance"
- "Dies if item dequeued out of order"
- "Dies if lower priority executes first"

## Output Template

```yaml
claims:
  - id: "001"
    type: ordering
    statement: "<X> ≤ <Y> under <conditions>"
    criteria:
      - "Dies if order violated between adjacent elements"
      - "Dies if transitivity broken"
    context:
      constraints: "<Comparison function, stability>"
      approach: "Verify order after operations"
```

## Testing Strategies

| Strategy | Method | Tools |
|----------|--------|-------|
| Comparison tests | Check pairwise order | pytest |
| Transitivity checks | Verify A<B, B<C → A<C | hypothesis |
| Stability tests | Equal elements preserve order | pytest |
| Concurrent tests | Order under race conditions | pytest |

## Common Mistakes

1. **Undefined comparison** — How exactly is order determined?
2. **Ignoring ties** — What happens with equal elements?
3. **Missing transitivity** — Order must be consistent
4. **Stability confusion** — Does insertion order matter for equals?
