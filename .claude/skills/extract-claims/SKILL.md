---
name: extract-claims
description: "Extract testable claims from existing codebases. Analyzes code, comments, docs, and tests to find implicit and explicit claims. Use when testing existing projects."
---

# Extract Claims

Find testable claims hiding in code.

## Process

1. **Scan project structure** — Identify key files and patterns
2. **Analyze sources** — Look for claims in each source type
3. **Classify claims** — contract, belief, or spark
4. **Rate confidence** — How certain is this claim?
5. **Deduplicate** — Merge similar claims
6. **Output** — Structured YAML

## Claim Sources

### Code Structure (Contract Claims)

| Pattern | Implied Claim |
|---------|---------------|
| `@require_auth` decorator | "Endpoint requires authentication" |
| `if not user.is_admin: raise 403` | "Non-admins get 403" |
| `return JsonResponse(status=201)` | "Successful creation returns 201" |
| Type hints | "Function accepts/returns these types" |
| Validation logic | "Invalid input is rejected" |

### Comments and Docs (Belief Claims)

| Pattern | Implied Claim |
|---------|---------------|
| `# This is fast because...` | Performance claim |
| `# Cache this for better performance` | Caching helps |
| README: "Handles 10k requests/sec" | Throughput claim |
| `# Users prefer X` | User behavior claim |

### Tests (Contract Claims)

| Pattern | Implied Claim |
|---------|---------------|
| `test_login_returns_401` | "Login can return 401" |
| `assert response.json()["error"]` | "Response includes error field" |
| Mocked behavior | "System depends on this behavior" |

### TODOs and FIXMEs (Spark Claims)

| Pattern | Implied Claim |
|---------|---------------|
| `# TODO: add caching` | "Caching would help" |
| `# FIXME: this is slow` | "This needs optimization" |
| `# Future: support X` | "X is feasible and valuable" |

## Scripts

- `scripts/extract.py` — Automated extraction from code

## References

- `references/patterns.md` — Detailed extraction patterns

## Output Format

```yaml
source:
  path: "<project path>"
  analyzed: "<timestamp>"

claims:
  - id: "001"
    type: contract | belief | spark
    statement: "<Testable claim>"
    source_file: "<file:line>"
    source_text: "<Original text that implied this>"
    confidence: high | medium | low
```

## Confidence Levels

- **high** — Explicit in code/docs, unambiguous
- **medium** — Inferable from patterns, some interpretation
- **low** — Speculative, based on weak signals
