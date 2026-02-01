# Feasibility Claim Refinement

Feasibility claims test whether X can work at all — new ideas, POCs, proof of concept.

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

### 4. Define Kill Criteria

What would prove this doesn't work?

Kill template: **Show blocker that prevents X from working**

Examples:
- "Dies if accuracy is at or below random chance (50%)"
- "Dies if core mechanism produces no measurable signal"
- "Dies if fundamental assumption is proven false"
- "Dies if required data/API doesn't exist"

## Output Template

```yaml
claims:
  - id: "001"
    type: feasibility
    statement: "<Clear feasibility question>"
    criteria:
      - "Dies if <specific blocker found>"
      - "Dies if <baseline not exceeded>"
    context:
      constraints: "<Time/resource limits, assumptions>"
      approach: "Build minimal POC that tests core mechanism"
      success_bar: "<What 'working' looks like>"
```

## Testing Strategies

| Strategy | Method | Tools |
|----------|--------|-------|
| POC build | Create minimal implementation | custom |
| Literature review | Check if already solved/impossible | web search |
| Expert consult | Get domain knowledge | human |
| Rapid prototype | Quick and dirty test | pytest |

## Common Mistakes

1. **Too ambitious** — Test the core mechanism, not the product
2. **Vague success** — "It works" isn't measurable
3. **No baseline** — Better than what?
4. **Scope creep** — Test ONE thing
5. **Ignoring blockers** — What could make this impossible?
