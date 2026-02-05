---
name: test-claim
description: "Attack claims with Veritas verification, capture observations, render verdicts. Use when falsifier needs to execute tests. Uses Analytic, Modal, Empirical, Probabilistic truth types."
---

# Test Claim

Attack claims using Veritas verification and render verdicts.

## Process

1. Load appropriate reference for truth type
2. Design the strongest attack (falsification strategy)
3. Execute the test using `claim()` context manager
4. Capture all observations as Evidence
5. Let Veritas verify: compare evidence to falsification form
6. Render verdict: KILLED | SURVIVED | UNCERTAIN
7. Identify mutations

## Veritas Verification Flow

```python
from veritas import claim, Analytic, Verdict

# 1. Define truth
truth = Analytic(
    statement="2+2=4",
    lhs="result",
    rhs=4,
)

# 2. Gather evidence with claim() context manager
with claim(truth) as c:
    actual = 2 + 2
    c.bind(result=actual, x=actual)

# 3. Veritas verifies automatically on exit
print(c.result.verdict)  # SURVIVED or KILLED
```

## Verdict Definitions

| Verdict | Meaning | When It Happens |
|---------|---------|-----------------|
| **KILLED** | Claim is false | Falsification form satisfied (∃counterexample) |
| **SURVIVED** | Claim held up | Falsification form not satisfied |
| **UNCERTAIN** | Can't determine | Missing evidence, symbolic cannot resolve |

## Testing by Truth Type

| Truth Type | Kill Target | Test Method |
|------------|-------------|-------------|
| Analytic | ∃x: X ≠ Y | Compare actual vs expected |
| Modal | ◇¬P | Search for invariant violation |
| Empirical | Contradicting obs | Observe and check predicate |
| Probabilistic | Threshold crossed | Measure metric, compare to threshold |

## Using claim() Context Manager

```python
from veritas import claim, Analytic, Modal, Empirical, Probabilistic, sym

# Analytic (equality)
with claim(Analytic("add works", lhs="result", rhs=4)) as c:
    c.bind(result=2+2, x=4)
assert c.result.verdict.name == "SURVIVED"

# Modal (invariant)
x = sym("x")
with claim(Modal("x >= 0", invariant=x >= 0)) as c:
    c.bind(state=5, x=5)
# Check c.result.verdict

# Empirical (observation)
with claim(Empirical("API returns 200", observation_var="status")) as c:
    status = make_api_call()
    c.bind(status=status)
# Check via truth.check_observation(status)

# Probabilistic (threshold)
with claim(Probabilistic("accuracy > 50%", metric="accuracy", threshold=0.5)) as c:
    acc = evaluate_model()
    c.bind(accuracy=acc)
# Check via truth.check_threshold(acc)
```

## Output Format

Update claims.yaml with VerdictResult:

```yaml
claims:
  - id: "001"
    truth_type: Analytic  # or Modal, Empirical, Probabilistic
    statement: "<Human-readable claim>"
    falsification_form: "∃x: result ≠ 4"
    test:
      method: "<What test was performed>"
      code: |
        from veritas import claim, Analytic

        with claim(Analytic("test", lhs="result", rhs=4)) as c:
            c.bind(result=actual_value, x=actual_value)
    observations:
      raw: |
        <Exact output from test>
      evidence:
        result: 4
        x: 4
    verdict: KILLED | SURVIVED | UNCERTAIN
    reasoning: "<Veritas reasoning from VerdictResult>"
    mutations:
      - "<New claim that emerged from this test>"
```

## References

- `references/equality.md` — Testing Analytic claims (equality/membership/ordering)
- `references/invariant.md` — Testing Modal claims (invariants)
- `references/grounding.md` — Testing Empirical claims (attribution)
- `references/feasibility.md` — Testing Empirical/Probabilistic claims (POC)

## Rules

1. **Run actual tests** — Use `claim()` context manager
2. **Capture evidence** — All bindings matter
3. **Strongest attack** — Try to kill the claim
4. **Let Veritas verify** — Don't manually determine verdicts
5. **Note the unexpected** — Surprises become mutations
