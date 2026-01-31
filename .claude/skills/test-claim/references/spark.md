# Testing Spark Claims

Spark claims require building something to test feasibility.

## Methodology

### 1. Build Minimal POC

Use the `build-poc` skill to create the smallest working prototype.

- Focus on core mechanism only
- Skip UI unless UI is the claim
- Use existing libraries/APIs where possible
- Time-box: hours, not days

### 2. Design the Test

What specific action will test the claim?

| Claim Type | Test Approach |
|------------|---------------|
| "Can detect X" | Collect samples, run detection, measure accuracy |
| "Can predict X" | Split data, train/test, compare to baseline |
| "Can build X" | Build it, measure if it works |
| "X is faster" | Benchmark both, compare |

### 3. Execute and Observe

Run the POC and capture:
- Exact output/results
- Error messages
- Performance metrics
- Unexpected behaviors

### 4. Compare to Kill Criteria

Go through each criterion:
- Is it clearly met? → KILLED
- All criteria unmet? → SURVIVED
- Can't determine? → UNCERTAIN

## Output Format

```yaml
test:
  method: "Built POC to <test mechanism>. Ran <specific test>."
  code: |
    # Actual runnable code
    import ...
    result = ...
    print(result)
observations:
  raw: |
    <Exact output>
  unexpected: "<Any surprises>"
verdict: KILLED | SURVIVED | UNCERTAIN
reasoning: "<Based on criteria X, because observation Y>"
mutations:
  - "<New claim that emerged>"
```

## Common Pitfalls

1. **Overcomplicated POC** — Test the mechanism, not the product
2. **Vague observations** — Capture exact numbers, not "it was slow"
3. **Moving goalposts** — Verdict based on pre-stated criteria only
4. **Ignoring failures** — Document what went wrong

## When to Use UNCERTAIN

- POC couldn't be built (blocked by external factor)
- Test was flawed (didn't actually test the claim)
- Results are ambiguous (need different test design)

UNCERTAIN is valid. It means "need more information."
