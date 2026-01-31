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

### Contract Claims

Found in:
- API route handlers
- Function signatures with type hints
- Error handling patterns
- Validation logic
- Test files (existing tests = implicit claims)

### Belief Claims

Found in:
- Comments mentioning performance
- TODO/FIXME notes
- Documentation claims
- README assertions
- Config values with implicit assumptions

### Spark Claims

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
    type: contract
    statement: "POST /api/users requires authentication"
    source_file: "routes/users.py:42"
    confidence: high

  - id: "002"
    type: belief
    statement: "Query caching improves response time"
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
5. Deduplicate and classify
6. Output structured claims
