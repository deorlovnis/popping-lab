# Grounding Claim Refinement → Empirical Truth

Grounding claims test that X is supported by Y. In Veritas, these become **Empirical** truths.

**Veritas Type:** `Empirical`
**Falsification Form:** Find observation that contradicts support

## Characteristics

- Claim requires traceable support
- Evidence must exist and be valid
- Chain of derivation matters
- Ungrounded claims are killed

## Refinement Process

### 1. Identify What Needs Grounding

What claim needs support?

| Vague | Sharp |
|-------|-------|
| "Tested code" | "All assertions have test coverage" |
| "Documented" | "Every public API has docstring" |
| "Based on research" | "Each cited paper exists and supports claim" |

### 2. Define Valid Support

Be explicit about:
- What counts as evidence
- How to trace from claim to support
- Minimum threshold (coverage %, citation count)
- Validity criteria for the support itself

### 3. Identify Gaps

Where might grounding be missing?
- New code without tests
- Undocumented edge cases
- Broken links/references
- Outdated sources
- Circular references

### 4. Set Falsification Form

For Empirical: **Find observation contradicting support**

Examples:
- "Observe: assertion without test"
- "Observe: public method without docstring"
- "Observe: citation that doesn't exist"

## Veritas Output Template

```python
from veritas import Empirical

# Test coverage
truth = Empirical(
    statement="All assertions have test coverage",
    observation_var="uncovered_assertion",
    expected_predicate=lambda x: x is None,  # No uncovered assertions
    contradiction_description="Found assertion without test",
)

# Documentation coverage
truth = Empirical(
    statement="All public methods have docstrings",
    observation_var="undocumented_method",
    expected_predicate=lambda x: x is None,
    contradiction_description="Found public method without docstring",
)

# Citation verification
truth = Empirical(
    statement="All citations exist and are accessible",
    observation_var="broken_citation",
    expected_predicate=lambda x: x is None,
    contradiction_description="Found citation that doesn't resolve",
)
```

## Testing Strategies

| Strategy | Method | Veritas Pattern |
|----------|--------|-----------------|
| Coverage analysis | Measure test coverage | pytest-cov + Empirical |
| Link checking | Verify references exist | requests + Empirical |
| Trace analysis | Follow derivation chain | custom + Empirical |
| Doc coverage | Check documentation | interrogate + Empirical |

## Common Mistakes

1. **Vague support criteria** — What exactly counts as evidence?
2. **Circular grounding** — A supports B supports A
3. **Stale references** — Support existed but was removed
4. **Weak support** — Evidence exists but doesn't actually support claim
