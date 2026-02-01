---
name: test-claim
description: "Attack claims with tests, capture observations, render verdicts. Use when falsifier needs to execute tests. Supports property-based types: equality, invariant, membership, ordering, grounding, feasibility."
---

# Test Claim

Attack claims and render verdicts.

## Process

1. Load appropriate reference for claim type
2. Design the strongest attack
3. Execute the test
4. Capture all observations
5. Compare to falsification criteria
6. Render verdict: KILLED | SURVIVED | UNCERTAIN
7. Identify mutations

## Verdict Definitions

| Verdict | Meaning | When to Use |
|---------|---------|-------------|
| **KILLED** | Claim is false | At least one kill criterion clearly met |
| **SURVIVED** | Claim held up | No criteria met, test was valid |
| **UNCERTAIN** | Can't determine | Test was flawed, blocked, or inconclusive |

## Property-Based Testing

| Type | Kill Target | Test Method |
|------|-------------|-------------|
| equality | Find X ≠ Y | Compare actual vs expected |
| invariant | Find ¬P | Search for constraint violation |
| membership | Find X ∉ S | Test element against set criteria |
| ordering | Find violation | Verify order relationships |
| grounding | Find ungrounded | Trace claims to evidence |
| feasibility | Show blocker | Build POC, identify blockers |

## Scripts

- `scripts/notebook.py` — Generate experiment notebook

## References

- `references/equality.md` — Testing X = Y claims
- `references/invariant.md` — Testing P always holds claims
- `references/membership.md` — Testing X ∈ S claims
- `references/ordering.md` — Testing X ≤ Y claims
- `references/grounding.md` — Testing attribution claims
- `references/feasibility.md` — POC testing (also load build-poc skill)

## Output Format

Update claims.yaml with test results:

```yaml
claims:
  - id: "001"
    # ... original fields preserved ...
    test:
      method: "<What test was performed>"
      code: |
        <Actual code that was run>
    observations:
      raw: |
        <Exact output from test>
      unexpected: "<Any surprises>"
    verdict: KILLED | SURVIVED | UNCERTAIN
    reasoning: "<Why this verdict based on criteria>"
    mutations:
      - "<New claim that emerged from this test>"
```

## Rules

1. **Run actual tests** — Don't just describe what you'd do
2. **Capture everything** — Raw output matters
3. **Strongest attack** — Try to kill the claim
4. **Be impartial** — Let evidence decide
5. **Note the unexpected** — Surprises are valuable
