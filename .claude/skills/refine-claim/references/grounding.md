# Grounding Claim Refinement

Grounding claims test that X is supported by Y — attribution, evidence, derivation.

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

### 4. Set Kill Criteria

What proves grounding is broken?

Kill template: **Find ungrounded X (claim without support)**

Examples:
- "Dies if any assertion lacks test"
- "Dies if public method undocumented"
- "Dies if citation doesn't exist"

## Output Template

```yaml
claims:
  - id: "001"
    type: grounding
    statement: "<X> is supported by <Y>"
    criteria:
      - "Dies if X found without supporting Y"
      - "Dies if Y doesn't actually support X"
    context:
      constraints: "<What counts as valid support>"
      approach: "Trace each X to its Y"
```

## Testing Strategies

| Strategy | Method | Tools |
|----------|--------|-------|
| Coverage analysis | Measure test coverage | pytest-cov |
| Link checking | Verify references exist | custom |
| Trace analysis | Follow derivation chain | custom |
| Doc coverage | Check documentation completeness | interrogate |

## Common Mistakes

1. **Vague support criteria** — What exactly counts as evidence?
2. **Circular grounding** — A supports B supports A
3. **Stale references** — Support existed but was removed
4. **Weak support** — Evidence exists but doesn't actually support claim
