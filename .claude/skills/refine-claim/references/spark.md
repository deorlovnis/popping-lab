# Spark Claim Refinement

Sparks are feasibility claims. Can this idea work at all?

## Characteristics

- Novel or unproven concept
- Requires building something to test
- Success measured by working demonstration
- Often starts vague, needs sharpening

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
- Time-box: if it takes more than a few hours, scope is too big

### 3. Set Success Criteria

What would convince you this works?

- Be specific: "accuracy > 60%" not "it works"
- Compare to baseline: "better than random" or "better than existing"
- Consider false positives: what looks like success but isn't?

### 4. Define Kill Criteria

What would prove this doesn't work?

Examples:
- "Dies if accuracy is at or below random chance (50%)"
- "Dies if it requires >10s to process a single request"
- "Dies if the core mechanism produces no measurable signal"

## Output Template

```yaml
claims:
  - id: "001"
    type: spark
    statement: "<Clear, testable feasibility statement>"
    criteria:
      - "Dies if <specific failure condition>"
      - "Dies if <another failure condition>"
    context:
      constraints: "<Time/resource limits, assumptions>"
      approach: "Build minimal POC that <tests core mechanism>"
      success_bar: "<What 'working' looks like>"
```

## Common Mistakes

1. **Too ambitious** — Test the core mechanism, not the product
2. **Vague success** — "It works" isn't measurable
3. **No baseline** — Better than what?
4. **Scope creep** — Test ONE thing
