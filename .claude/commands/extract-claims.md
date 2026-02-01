---
name: extract-claims
description: Extract testable claims from a codebase without running tests. Analyzes code, comments, docs for implicit and explicit claims.
---

# /extract-claims

Extract claims from a codebase without running tests.

## Usage

```
/extract-claims <project-path>
/extract-claims <project-path> --output <file>
```

## Arguments

- `<project-path>` — Path to the codebase to analyze
- `--output` — Save claims to file (default: prints to stdout)

## What Gets Extracted

### Equality Claims

Found in:
- API route handlers (expected responses)
- Function signatures with type hints
- Test assertions (expected = actual)

### Invariant Claims

Found in:
- Comments mentioning performance bounds
- Constraint assertions
- Config values with limits
- Documentation claims about guarantees

### Membership Claims

Found in:
- Validation logic
- Type hints
- Enum definitions
- Input sanitization

### Ordering Claims

Found in:
- Sorting logic
- Queue implementations
- Comments about priority

### Grounding Claims

Found in:
- Documentation references
- Test coverage expectations
- Citation comments

### Feasibility Claims

Found in:
- Comments about future features
- TODO items for new functionality
- Architecture decision records

## Examples

```bash
# Extract claims and print to stdout
/extract-claims ~/my-project

# Save to file
/extract-claims ~/my-project --output claims.yaml

# Then test them
/test-claim ~/my-project
```

## Output Format

```yaml
# claims.yaml
source:
  path: "/path/to/project"
  analyzed: "2024-01-15T10:30:00"

claims:
  - id: "001"
    type: equality
    statement: "POST /api/users returns 401 without auth"
    source_file: "routes/users.py:42"
    confidence: high

  - id: "002"
    type: invariant
    statement: "Query caching improves response time by >30%"
    source_file: "services/db.py:15"
    source_text: "# Cache this for performance"
    confidence: medium
```

## Process

This command uses the **extract-claims** skill to:

1. Scan project structure
2. Analyze code patterns
3. Extract explicit claims (from docs, comments)
4. Infer implicit claims (from code structure)
5. Classify by property type
6. Deduplicate and output
