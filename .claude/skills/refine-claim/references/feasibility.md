# Feasibility Claim Refinement → Empirical/Probabilistic Truth

Feasibility claims test whether X can work at all. In Veritas, these become **Empirical** (for blockers) or **Probabilistic** (for thresholds) truths.

**Veritas Types:** `Empirical` or `Probabilistic`
**Falsification Forms:**
- Empirical: Observe blocker that prevents X from working
- Probabilistic: Metric fails to meet threshold

## Characteristics

- Novel or unproven concept
- Requires building something to test
- Success measured by working demonstration
- Blockers prove infeasibility

## Refinement Process

### 1. Extract the Core Question

What's the actual thing being tested?

| Vague | Sharp |
|-------|-------|
| "AI could help with coding" | "Can GPT-4 fix simple bugs from error messages alone?" |
| "Predict mood from typing" | "Can typing speed variance predict self-reported stress level?" |
| "Better search" | "Can semantic search outperform keyword search for code queries?" |

### 2. Define Minimum Viable Test

What's the smallest thing you could build to get signal?

- Strip all nice-to-haves
- Focus on the core mechanism
- Time-box: if it takes too long, scope is too big

### 3. Set Success Criteria

What would convince you this works?

- Be specific: "accuracy > 60%" not "it works"
- Compare to baseline: "better than random" or "better than existing"
- Consider false positives: what looks like success but isn't?

### 4. Choose Truth Type

**Use Empirical when:**
- Looking for blockers (API doesn't exist, data unavailable)
- Success is binary (works/doesn't work)
- Observation contradicts feasibility

**Use Probabilistic when:**
- Success has a threshold (accuracy > X)
- Comparing to baseline
- Measuring continuous metric

## Veritas Output Templates

### For Blocker Detection (Empirical)

```python
from veritas import Empirical

truth = Empirical(
    statement="Can build typing-based stress predictor",
    observation_var="blocker",
    expected_predicate=lambda x: x is None,  # No blocker found
    contradiction_description="Found blocker preventing implementation",
)
```

### For Threshold Testing (Probabilistic)

```python
from veritas import Probabilistic

# Accuracy threshold
truth = Probabilistic(
    statement="Model accuracy > 60%",
    metric="accuracy",
    threshold=0.6,
    direction=">",
)

# Better than baseline
truth = Probabilistic(
    statement="Semantic search recall > keyword baseline",
    metric="recall_improvement",
    threshold=0.0,  # > 0 means better than baseline
    direction=">",
)
```

## Testing Strategies

| Strategy | Method | Veritas Pattern |
|----------|--------|-----------------|
| POC build | Create minimal implementation | Empirical (blocker check) |
| Accuracy test | Evaluate model | Probabilistic (threshold) |
| A/B comparison | Compare to baseline | Probabilistic (improvement) |
| Resource check | Verify feasibility | Empirical (constraint check) |

## Common Blockers

| Blocker Type | Example | Truth Type |
|--------------|---------|------------|
| Data unavailable | API deprecated, no training data | Empirical |
| Below baseline | Accuracy ≤ random chance | Probabilistic |
| Resource constraint | Takes days to run, needs GPU | Empirical |
| Fundamental limit | Violates physics/math | Empirical |
| External dependency | Required service doesn't exist | Empirical |

## Common Mistakes

1. **Too ambitious** — Test the core mechanism, not the product
2. **Vague success** — "It works" isn't measurable
3. **No baseline** — Better than what?
4. **Scope creep** — Test ONE thing
5. **Ignoring blockers** — What could make this impossible?
