---
name: refine-claim
description: "Sharpen fuzzy ideas into testable, falsifiable claims using Veritas truth types. Use when claimer needs to transform raw ideas. Maps to: Analytic, Modal, Empirical, Probabilistic."
---

# Refine Claim

Transform fuzzy ideas into sharp, falsifiable claims using Veritas truth types.

## Process

1. Determine truth type from the claim's nature
2. Load appropriate reference:
   - `references/equality.md` for equality/membership/ordering claims → **Analytic**
   - `references/invariant.md` for constraint/bounds claims → **Modal**
   - `references/grounding.md` for attribution/evidence claims → **Empirical**
   - `references/feasibility.md` for POC/threshold claims → **Empirical** or **Probabilistic**
3. Follow the refinement process in that reference
4. Output Veritas truth type with falsification form

## Veritas Truth Types

| Truth Type | What It Tests | Falsification Form |
|------------|---------------|-------------------|
| **Analytic** | X = Y, X ∈ S, X ≤ Y | ∃x: f(x) ≠ expected |
| **Modal** | P always holds | ◇¬P (find state where ¬P) |
| **Empirical** | Observation supports claim | Find contradicting observation |
| **Probabilistic** | P(X) op threshold | Find metric violating threshold |

## Mapping Old Types → Veritas

| Old Type | Veritas Truth | Rationale |
|----------|---------------|-----------|
| equality | `Analytic` | ∃x: f(x) ≠ expected |
| membership | `Analytic` | ∃x: x ∉ S (element fails predicate) |
| ordering | `Analytic` | ∃x,y: order(x,y) violated |
| invariant | `Modal` | ◇¬P (possible violation) |
| grounding | `Empirical` | observation contradicts support |
| feasibility | `Empirical`/`Probabilistic` | blocker or threshold violation |

## Key Principles

### Falsifiability

A claim must be specific enough to be wrong.

Bad: "Caching helps performance"
Good: "Redis caching reduces p95 latency by >40% for read-heavy endpoints"

### Kill Criteria via Falsification Form

The falsification form states what would prove the claim false.

Examples:
- Analytic: "∃x: add(x, 2) ≠ x + 2"
- Modal: "◇(balance < 0) — find state where balance negative"
- Empirical: "Observation shows API returns non-200"
- Probabilistic: "accuracy ≤ 0.5 — not better than random"

### Minimum Scope

Find the smallest version that answers the core question.

- Strip nice-to-haves
- Focus on core hypothesis
- Time-box the test

## Output Template

```python
from veritas import Analytic, Modal, Empirical, Probabilistic

# For equality/membership/ordering:
truth = Analytic(
    statement="<Clear statement>",
    lhs="<variable name>",
    rhs=<expected value>,
)

# For invariants:
truth = Modal(
    statement="<Property always holds>",
    invariant=<sympy predicate>,
)

# For grounding/observation:
truth = Empirical(
    statement="<Observation-based claim>",
    observation_var="<what we observe>",
    expected_predicate=lambda x: <condition>,
)

# For thresholds:
truth = Probabilistic(
    statement="<Metric claim>",
    metric="<metric name>",
    threshold=<value>,
    direction=">",  # or ">=", "<", "<=", "="
)
```

## References

- `references/equality.md` — Equality/membership/ordering → Analytic
- `references/invariant.md` — Invariants → Modal
- `references/grounding.md` — Attribution/evidence → Empirical
- `references/feasibility.md` — POC/thresholds → Empirical/Probabilistic
