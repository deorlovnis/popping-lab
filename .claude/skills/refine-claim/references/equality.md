# Equality Claim Refinement

Equality claims test that X equals Y — comparisons, return values, expected outputs.

## Characteristics

- Specific input → expected output
- Deterministic (same input = same result)
- Direct comparison possible
- Can write assertion that passes/fails

## Refinement Process

### 1. Identify the Equality

What two things are being compared?

| Vague | Sharp |
|-------|-------|
| "Login should work" | "POST /login with valid credentials returns 200" |
| "Parser works" | "parse('2024-01-01') returns Date(2024, 1, 1)" |
| "Math is correct" | "add(2, 2) equals 4" |

### 2. Specify Both Sides

Be explicit about:
- Left side: actual result (function call, API response, output)
- Right side: expected value (literal, computed, schema)
- Comparison method (==, deep equals, schema match)

### 3. Define Test Inputs

What inputs will be tested?
- Happy path inputs
- Edge cases (empty, null, max)
- Boundary values
- Invalid inputs (if applicable)

### 4. Set Kill Criteria

What proves equality is broken?

Kill template: **Find input where X ≠ Y**

Examples:
- "Dies if status code is not 200"
- "Dies if output differs from expected"
- "Dies if any test case shows inequality"

## Output Template

```yaml
claims:
  - id: "001"
    type: equality
    statement: "<X> equals <Y> when <condition>"
    criteria:
      - "Dies if X ≠ Y for input <case>"
      - "Dies if comparison fails on edge case"
    context:
      constraints: "<Test environment, setup>"
      approach: "Call <X>, compare to <Y>"
```

## Testing Strategies

| Strategy | Method | Tools |
|----------|--------|-------|
| Unit test | Assert X == Y | pytest |
| Property test | For all inputs, X == Y | hypothesis |
| Formal proof | Prove X = Y algebraically | sympy, z3 |

## Common Mistakes

1. **Vague expected value** — "returns success" vs "returns {'ok': true}"
2. **Missing edge cases** — What about empty input?
3. **Wrong comparison** — Reference equality vs value equality
4. **Floating point** — Use approximate equality for floats
