# Testing Membership Claims → Analytic Verification

Membership claims are tested using **Analytic** truths in Veritas.

**Kill target:** ∃x: x ∉ S (find element outside expected set)

## Methodology

### 1. Define the Set

What is S exactly?
- Enumeration: {admin, user, guest}
- Pattern: RFC 5322 email format
- Schema: JSON with required fields
- Type: positive integers

### 2. Design Test Cases

Test both sides of the boundary:
- **Valid elements** — Should be accepted
- **Invalid elements** — Should be rejected
- **Edge cases** — On the boundary

### 3. Execute with Veritas

```python
from veritas import claim, Analytic, Verdict

# Define membership as equality check
truth = Analytic(
    statement="role is valid (admin, user, or guest)",
    lhs="is_valid",
    rhs=True,
)

def is_valid_role(role):
    return role in {"admin", "user", "guest"}

# Test valid case
with claim(truth) as c:
    result = is_valid_role("admin")
    c.bind(is_valid=result, x=result)

assert c.result.verdict == Verdict.SURVIVED

# Test invalid case
with claim(truth) as c:
    result = is_valid_role("superuser")
    c.bind(is_valid=result, x=result)

assert c.result.verdict == Verdict.KILLED  # Found non-member accepted
```

### 4. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Invalid element accepted | KILLED |
| Valid element rejected | KILLED |
| All classifications correct | SURVIVED |

## Testing Patterns

### Enum Membership

```python
from veritas import claim, Analytic

VALID_ROLES = {"admin", "user", "guest"}

truth = Analytic(
    statement="role is in valid set",
    lhs="is_member",
    rhs=True,
)

def test_role_membership():
    # Test valid
    with claim(truth) as c:
        c.bind(is_member="admin" in VALID_ROLES, x=True)
    assert c.result.verdict == Verdict.SURVIVED

    # Test invalid
    with claim(truth) as c:
        c.bind(is_member="superuser" in VALID_ROLES, x=False)
    assert c.result.verdict == Verdict.KILLED
```

### Pattern Membership

```python
from veritas import claim, Analytic
import re

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

truth = Analytic(
    statement="email matches valid pattern",
    lhs="is_valid",
    rhs=True,
)

def test_email_membership():
    valid_emails = ["user@example.com", "test.name@domain.org"]
    invalid_emails = ["@missing.com", "no-at-sign", "a@.com"]

    for email in valid_emails:
        with claim(truth) as c:
            c.bind(is_valid=bool(re.match(EMAIL_PATTERN, email)), x=True)
        assert c.result.verdict == Verdict.SURVIVED, f"Valid rejected: {email}"

    for email in invalid_emails:
        with claim(truth) as c:
            c.bind(is_valid=bool(re.match(EMAIL_PATTERN, email)), x=True)
        # Expect KILLED because invalid emails should NOT match
```

### Schema Membership

```python
from veritas import claim, Analytic

truth = Analytic(
    statement="response has required 'id' field",
    lhs="has_id",
    rhs=True,
)

with claim(truth) as c:
    response = api_call()
    has_id = "id" in response and isinstance(response["id"], int)
    c.bind(has_id=has_id, x=has_id)
```

### Range Membership

```python
from veritas import claim, Analytic

truth = Analytic(
    statement="value in range [0, 100]",
    lhs="in_range",
    rhs=True,
)

def test_range_membership():
    test_cases = [
        (50, True),   # In range
        (0, True),    # Lower bound
        (100, True),  # Upper bound
        (-1, False),  # Below range
        (101, False), # Above range
    ]

    for value, expected in test_cases:
        with claim(truth) as c:
            in_range = 0 <= value <= 100
            c.bind(in_range=in_range, x=in_range)
```

## Tips

1. **Test both directions** — False positives AND false negatives
2. **Edge cases matter** — Empty strings, boundary values
3. **Use property testing** — Generate random elements
4. **Document the set** — Be explicit about membership criteria
