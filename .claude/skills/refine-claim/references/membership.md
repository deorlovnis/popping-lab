# Membership Claim Refinement → Analytic Truth

Membership claims test that X belongs to set S. In Veritas, these become **Analytic** truths with a membership predicate.

**Veritas Type:** `Analytic`
**Falsification Form:** ∃x: x ∉ S (element fails membership test)

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

### 4. Set Falsification Form

For Analytic (membership): **∃x: is_member(x) ≠ True**

Examples:
- "∃email: is_valid_email(email) = False for valid input"
- "∃role: role ∉ {admin, user, guest}"
- "∃response: 'id' not in response"

## Veritas Output Template

```python
from veritas import Analytic

# Enum membership
truth = Analytic(
    statement="role is valid (admin, user, or guest)",
    lhs="is_valid_role",
    rhs=True,
)

# Pattern membership
truth = Analytic(
    statement="email matches RFC 5322 format",
    lhs="is_valid_email",
    rhs=True,
)

# Schema membership
truth = Analytic(
    statement="response has required 'id' field",
    lhs="has_id_field",
    rhs=True,
)

# Range membership
truth = Analytic(
    statement="value in range [0, 100]",
    lhs="in_range",
    rhs=True,
)
```

## Testing Strategies

| Strategy | Method | Veritas Pattern |
|----------|--------|-----------------|
| Validation tests | Check known in/out cases | `claim(Analytic(...))` |
| Edge case testing | Test boundaries | pytest + Analytic |
| Property testing | Generate random elements | hypothesis + Analytic |
| Type checking | Static analysis | mypy + Analytic |

## Common Mistakes

1. **Vague set definition** — "valid" without criteria
2. **Missing exclusions** — Only testing what's in
3. **Incomplete enumeration** — Missing edge cases
4. **Schema drift** — Set definition changed but tests didn't
