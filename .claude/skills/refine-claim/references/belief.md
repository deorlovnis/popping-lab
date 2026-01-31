# Belief Claim Refinement

Beliefs are assumptions about system behavior, performance, or the world.

## Characteristics

- May or may not be based on data
- Often about performance, scale, user behavior
- Requires measurement or evidence to test
- May have been true once but needs verification

## Refinement Process

### 1. Make the Belief Explicit

What exactly is being assumed?

| Vague | Sharp |
|-------|-------|
| "Caching helps" | "Redis caching reduces p95 latency by >40% for read-heavy endpoints" |
| "Users prefer X" | ">60% of users click the blue button over the red one" |
| "This is slow" | "The search query takes >500ms for >10k records" |

### 2. Quantify the Claim

Add numbers:
- By how much?
- Compared to what baseline?
- Under what conditions?
- For what population?

### 3. Identify Evidence Sources

How could this be tested?
- Existing metrics/logs
- A/B test results
- Benchmarks
- User research data
- Code analysis

### 4. Set Kill Criteria

What would prove the belief false?

Examples:
- "Dies if latency improvement is <20%"
- "Dies if preference is <50% (no better than random)"
- "Dies if no correlation found (p > 0.05)"

## Output Template

```yaml
claims:
  - id: "001"
    type: belief
    statement: "<Quantified claim about behavior/performance>"
    criteria:
      - "Dies if improvement is less than <threshold>"
      - "Dies if effect is not statistically significant"
      - "Dies if <contradicting evidence found>"
    context:
      constraints: "<Data availability, measurement period>"
      approach: "<How to measure/gather evidence>"
      baseline: "<What we're comparing against>"
```

## Evidence Types

| Belief Type | Evidence Approach |
|-------------|-------------------|
| Performance | Benchmarks, profiling, metrics |
| User behavior | Analytics, A/B tests, surveys |
| Code quality | Static analysis, test coverage |
| Scalability | Load testing, stress testing |

## Common Mistakes

1. **No baseline** — "40% faster" than what?
2. **Confirmation bias** — Seek disconfirming evidence
3. **Small samples** — Is the data representative?
4. **Outdated data** — When was this measured?
5. **Correlation ≠ causation** — What else could explain this?
