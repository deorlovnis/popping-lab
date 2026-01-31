---
name: build-poc
description: "Build minimal proof-of-concept implementations for spark claims. Creates runnable POCs in the experiment's poc/ directory."
---

# Build POC

Build minimal proofs of concept.

## POC Principles

1. **Minimal** — Only what's needed to test the claim
2. **Fast** — Hours, not days
3. **Disposable** — Not production code
4. **Observable** — Produces measurable output

## Output Location

POC code goes to: `lab/<experiment>/poc/`

## Process

1. Identify the core mechanism to test
2. Choose appropriate POC type (API, web, CLI, etc.)
3. Load relevant reference for patterns
4. Build the minimum working code
5. Add measurement/output capability
6. Document how to run it

## POC Structure

```
poc/
├── main.py           # Entry point
├── requirements.txt  # Dependencies (if any)
└── README.md         # How to run
```

## References

- `references/web.md` — Web app POCs
- `references/api.md` — API POCs
- `references/performance.md` — Performance POCs

## Quick Patterns

### Python Script POC
```python
#!/usr/bin/env python3
"""POC for: <claim>"""

def main():
    # Core mechanism
    result = test_the_thing()

    # Observable output
    print(f"Result: {result}")
    print(f"Success: {result > threshold}")

if __name__ == '__main__':
    main()
```

### API Call POC
```python
#!/usr/bin/env python3
import requests

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
print(f"Body: {response.json()}")
```

## Rules

- Every POC must be runnable
- Every POC must produce measurable output
- Document dependencies
- Don't gold-plate
