# Invariant Claim Refinement

Invariant claims test that property P always holds — bounds, constraints, guarantees.

## Characteristics

- Property must hold across ALL states/inputs
- Often about bounds, constraints, performance
- Requires searching for violations
- Single counterexample kills the claim

## Refinement Process

### 1. Identify the Invariant

What property must always be true?

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

### 4. Set Kill Criteria

What proves the invariant is broken?

Kill template: **Find state where ¬P**

Examples:
- "Dies if balance becomes negative"
- "Dies if latency exceeds 100ms"
- "Dies if data race detected"

## Output Template

```yaml
claims:
  - id: "001"
    type: invariant
    statement: "<P> holds under <conditions>"
    criteria:
      - "Dies if P violated in state <X>"
      - "Dies if bound exceeded under <condition>"
    context:
      constraints: "<Measurement period, environment>"
      approach: "Search for states where ¬P"
      baseline: "<Comparison point if applicable>"
```

## Testing Strategies

| Strategy | Method | Tools |
|----------|--------|-------|
| Fuzz testing | Random inputs seeking violation | hypothesis |
| Boundary testing | Test at limits | pytest |
| SMT solving | Prove no violation exists | z3-solver |
| Load testing | Stress test for performance bounds | pytest |

## Common Mistakes

1. **No quantification** — "fast" vs "< 100ms"
2. **Missing conditions** — Under what load?
3. **Single test** — Invariants need exhaustive search
4. **Wrong scope** — Does it hold always or usually?
5. **Correlation ≠ causation** — Is the bound causal?
