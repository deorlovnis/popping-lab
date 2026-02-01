# Testing Membership Claims

Membership claims test whether elements belong to expected sets.

Kill target: **Find X ∉ S (element outside expected set)**

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

### 3. Execute Tests

**Enum membership:**
```python
VALID_ROLES = {"admin", "user", "guest"}

def test_role_membership():
    assert validate_role("admin") == True
    assert validate_role("superuser") == False  # Not in set
```

**Pattern membership:**
```python
import re

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def test_email_membership():
    assert re.match(EMAIL_PATTERN, "user@example.com")
    assert not re.match(EMAIL_PATTERN, "not-an-email")
```

**Schema membership:**
```python
def test_response_membership():
    response = api_call()
    assert "id" in response  # Required field
    assert isinstance(response["id"], int)  # Correct type
```

### 4. Capture Observations

Record:
- Valid elements correctly accepted
- Invalid elements correctly rejected
- Any misclassifications (kills the claim)

### 5. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Invalid element accepted | KILLED |
| Valid element rejected | KILLED |
| All classifications correct | SURVIVED |

## Output Format

```yaml
test:
  method: "Tested email validation against RFC 5322"
  code: |
    valid = ["a@b.com", "user.name@domain.org"]
    invalid = ["@missing.com", "no-at-sign", "a@.com"]

    for email in valid:
        assert validate(email), f"False negative: {email}"
    for email in invalid:
        assert not validate(email), f"False positive: {email}"
observations:
  raw: |
    Valid emails: all accepted
    Invalid emails: "a@.com" was incorrectly accepted
  unexpected: "Domain starting with dot passes validation"
verdict: KILLED
reasoning: "Invalid email 'a@.com' was accepted (X ∉ S accepted as member)"
```

## Membership Testing Patterns

### Type Checking
```python
assert isinstance(value, expected_type)
```

### Enum Validation
```python
from enum import Enum

class Role(Enum):
    ADMIN = "admin"
    USER = "user"

assert role in Role.__members__
```

### Range Membership
```python
assert 0 <= value <= 100, "Value out of range [0, 100]"
```

## Tips

1. **Test both directions** — False positives AND false negatives
2. **Edge cases matter** — Empty strings, boundary values
3. **Use property testing** — Generate random elements
4. **Document the set** — Be explicit about membership criteria
