# Claim Extraction Patterns

Detailed patterns for finding claims in code.

## Contract Claim Patterns

### HTTP/API Patterns

```python
# Status codes
return Response(status=201)          # "Returns 201 on success"
raise Http404("Not found")           # "Returns 404 when not found"
return JsonResponse(data, status=200) # "Returns 200 with JSON"

# Auth decorators
@login_required                       # "Requires login"
@permission_required('admin')         # "Requires admin permission"
@require_http_methods(['POST'])       # "Only accepts POST"

# Validation
if not data.get('email'):            # "Email is required"
    raise ValidationError(...)
```

### Function Behavior Patterns

```python
# Type hints
def process(data: list[int]) -> dict:  # "Accepts list of ints, returns dict"

# Docstrings
def calculate(x: int) -> int:
    """
    Returns the square of x.           # "Returns square of input"
    Raises ValueError if x < 0.        # "Raises ValueError for negative"
    """

# Assertions
assert len(items) > 0                  # "Items must not be empty"
```

### Error Handling Patterns

```python
try:
    result = external_api.call()
except TimeoutError:
    return default_value                # "Falls back on timeout"
except APIError as e:
    log.error(e)
    raise                               # "Propagates API errors"
```

## Belief Claim Patterns

### Performance Comments

```python
# This is O(n) so should be fast       # Performance claim
# Caching this reduced latency by 50%  # Quantified improvement claim
# Fast path for common case            # Optimization assumption
```

### Assumption Comments

```python
# Users typically have < 100 items     # Scale assumption
# This should rarely happen            # Frequency assumption
# Most requests are reads              # Usage pattern assumption
```

### Architecture Comments

```python
# Using Redis because it's faster     # Technology choice rationale
# Async for better throughput         # Design decision belief
# Denormalized for read performance   # Trade-off belief
```

## Spark Claim Patterns

### TODOs

```python
# TODO: Add caching for performance    # "Caching would help"
# TODO: Support batch operations       # "Batch ops are feasible"
# TODO: Implement search               # "Search is needed and possible"
```

### FIXMEs

```python
# FIXME: This is slow for large inputs # "Needs optimization"
# FIXME: Race condition possible       # "Concurrency issue exists"
# FIXME: Doesn't handle edge case X    # "Edge case needs handling"
```

### Future Ideas

```python
# Future: ML-based recommendations     # "ML recs are feasible"
# Idea: Real-time notifications        # "Real-time is possible"
# v2: GraphQL support                  # "GraphQL is viable"
```

## Test File Patterns

### Test Names

```python
def test_login_returns_401_for_invalid_password():
    # Implies: "Invalid password returns 401"

def test_user_can_update_own_profile():
    # Implies: "Users can update their profile"

def test_admin_can_delete_any_user():
    # Implies: "Admins have delete permission"
```

### Assertions

```python
assert response.status_code == 201     # "Returns 201"
assert 'error' in response.json()      # "Error responses have error field"
assert len(results) <= 100             # "Results are paginated to 100"
```

### Mocks

```python
@mock.patch('app.external_api.call')   # "Depends on external API"
@mock.patch('app.cache.get')           # "Uses caching"
```

## Documentation Patterns

### README Claims

```markdown
- Handles 10,000 requests per second   # Throughput claim
- 99.9% uptime                         # Reliability claim
- Sub-millisecond latency              # Performance claim
- Supports PostgreSQL and MySQL        # Compatibility claim
```

### API Documentation

```markdown
Returns 401 if authentication fails    # Auth behavior
Rate limited to 100 requests/minute    # Rate limit claim
Response time < 200ms                  # SLA claim
```

## Confidence Assessment

### High Confidence

- Explicit code behavior (status codes, exceptions)
- Type hints and contracts
- Existing tests
- Clear documentation

### Medium Confidence

- Comments about behavior
- Inferred from code patterns
- Docstrings without tests

### Low Confidence

- TODOs and FIXMEs
- Vague comments
- Speculation about future
