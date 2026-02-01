# Membership Claim Refinement

Membership claims test that X belongs to set S — validation, filtering, classification.

## Characteristics

- Element must satisfy set criteria
- Clear set definition required
- Boundary between in/out matters
- Can enumerate or describe the set

## Refinement Process

### 1. Identify the Set

What set is the element supposed to belong to?

| Vague | Sharp |
|-------|-------|
| "Valid email" | "Matches RFC 5322 email pattern" |
| "Allowed role" | "role ∈ {admin, user, guest}" |
| "Correct type" | "Response is JSON object with 'id' field" |

### 2. Define Set Boundaries

Be explicit about:
- Inclusion criteria (what makes X ∈ S)
- Exclusion criteria (what makes X ∉ S)
- Edge cases (borderline elements)
- Set representation (enum, pattern, schema)

### 3. Identify Test Cases

What elements should be tested?
- Clearly valid (definitely in)
- Clearly invalid (definitely out)
- Edge cases (barely in/out)
- Malformed (wrong type entirely)

### 4. Set Kill Criteria

What proves membership is wrong?

Kill template: **Find X ∉ S (element outside expected set)**

Examples:
- "Dies if invalid email passes validation"
- "Dies if unknown role is accepted"
- "Dies if response missing required field"

## Output Template

```yaml
claims:
  - id: "001"
    type: membership
    statement: "<X> belongs to <S> when <condition>"
    criteria:
      - "Dies if X ∉ S for valid input"
      - "Dies if X ∈ S for invalid input"
    context:
      constraints: "<Set definition, schema>"
      approach: "Test membership for edge cases"
```

## Testing Strategies

| Strategy | Method | Tools |
|----------|--------|-------|
| Validation tests | Check known in/out cases | pytest |
| Edge case testing | Test boundaries | pytest |
| Property testing | Generate random elements | hypothesis |
| Type checking | Static analysis | mypy |

## Common Mistakes

1. **Vague set definition** — "valid" without criteria
2. **Missing exclusions** — Only testing what's in
3. **Incomplete enumeration** — Missing edge cases
4. **Schema drift** — Set definition changed but tests didn't
