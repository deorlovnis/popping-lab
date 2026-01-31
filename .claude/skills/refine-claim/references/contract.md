# Contract Claim Refinement

Contracts are claims about code behavior. They can be tested directly.

## Characteristics

- Specific input → expected output
- Can write a test that passes/fails
- Often involves APIs, functions, error handling
- Deterministic (same input = same result)

## Refinement Process

### 1. Identify the Contract

What behavior is being claimed?

| Vague | Sharp |
|-------|-------|
| "Login should work" | "POST /login with valid credentials returns 200 and JWT" |
| "Handle errors properly" | "Invalid JSON body returns 400 with error message" |
| "Fast response" | "GET /users responds in <100ms for <1000 users" |

### 2. Specify Input/Output

Be explicit about:
- Exact endpoint/function
- Input format and values
- Expected response (status, body, headers)
- Edge cases that matter

### 3. Define Boundary Conditions

What are the edges?
- Empty input
- Maximum size
- Invalid types
- Missing required fields
- Unauthorized access

### 4. Set Kill Criteria

What proves this contract is broken?

Examples:
- "Dies if status code is not 401"
- "Dies if response body lacks 'error' field"
- "Dies if function doesn't throw on null input"

## Output Template

```yaml
claims:
  - id: "001"
    type: contract
    statement: "<METHOD> <endpoint/function> with <input> returns/throws <output>"
    criteria:
      - "Dies if status code is not <expected>"
      - "Dies if response missing <field>"
      - "Dies if <edge case> not handled"
    context:
      constraints: "<Auth requirements, test environment>"
      approach: "Call endpoint with <input>, verify <output>"
```

## Testing Approaches

| Contract Type | Test Method |
|---------------|-------------|
| REST API | HTTP client (requests, curl) |
| Function | Unit test with assertions |
| CLI | Subprocess with args |
| Database | Query and verify |

## Common Mistakes

1. **Too broad** — "API works" is not testable
2. **Missing edge cases** — What about errors?
3. **Implicit assumptions** — State auth, environment
4. **No negative tests** — Also test what should fail
