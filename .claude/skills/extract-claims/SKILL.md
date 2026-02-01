---
name: extract-claims
description: "Extract testable claims from existing codebases. Analyzes code, comments, docs, and tests to find implicit and explicit claims. Use when testing existing projects."
---

# Extract Claims

Find testable claims hiding in code.

## Process

1. **Scan project structure** — Identify key files and patterns
2. **Analyze sources** — Look for claims in each source type
3. **Classify claims** — by property type
4. **Rate confidence** — How certain is this claim?
5. **Deduplicate** — Merge similar claims
6. **Output** — Structured YAML

## Claim Sources

### Code Structure (Equality/Invariant Claims)

| Pattern | Implied Claim | Type |
|---------|---------------|------|
| `@require_auth` decorator | "Endpoint requires authentication" | equality |
| `if not user.is_admin: raise 403` | "Non-admins get 403" | equality |
| `return JsonResponse(status=201)` | "Successful creation returns 201" | equality |
| Type hints | "Function accepts/returns these types" | membership |
| `assert balance >= 0` | "Balance never negative" | invariant |

### Comments and Docs (Invariant/Grounding Claims)

| Pattern | Implied Claim | Type |
|---------|---------------|------|
| `# This is fast because...` | Performance bound | invariant |
| `# Cache this for better performance` | Caching helps | invariant |
| README: "Handles 10k requests/sec" | Throughput claim | invariant |
| `# Sorted by relevance` | Order maintained | ordering |

### Tests (Equality/Membership Claims)

| Pattern | Implied Claim | Type |
|---------|---------------|------|
| `test_login_returns_401` | "Login returns 401" | equality |
| `assert response.json()["error"]` | "Response includes error field" | membership |
| Mocked behavior | "System depends on this behavior" | grounding |

### TODOs and FIXMEs (Feasibility Claims)

| Pattern | Implied Claim | Type |
|---------|---------------|------|
| `# TODO: add caching` | "Caching would help" | feasibility |
| `# FIXME: this is slow` | "This needs optimization" | invariant |
| `# Future: support X` | "X is feasible" | feasibility |

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
    type: equality | invariant | membership | ordering | grounding | feasibility
    statement: "<Testable claim>"
    source_file: "<file:line>"
    source_text: "<Original text that implied this>"
    confidence: high | medium | low
```

## Confidence Levels

- **high** — Explicit in code/docs, unambiguous
- **medium** — Inferable from patterns, some interpretation
- **low** — Speculative, based on weak signals
