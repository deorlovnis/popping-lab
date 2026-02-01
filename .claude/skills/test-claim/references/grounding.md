# Testing Grounding Claims

Grounding claims test that assertions are supported by evidence.

Kill target: **Find ungrounded X (claim without support)**

## Methodology

### 1. Identify What Needs Grounding

What claims need evidence?
- Code assertions need test coverage
- Documentation needs to match implementation
- Citations need to exist and support claims

### 2. Define Valid Support

What counts as evidence?
- Test that exercises the assertion
- Documentation that describes the behavior
- Citation that exists and is relevant

### 3. Execute Grounding Checks

**Test coverage:**
```python
import subprocess

# Run coverage analysis
result = subprocess.run(
    ["pytest", "--cov=src", "--cov-report=term-missing"],
    capture_output=True,
    text=True
)

# Check for uncovered assertions
print(result.stdout)
# Look for lines with 'assert' that show as uncovered
```

**Documentation coverage:**
```python
import ast
import inspect

def check_docstrings(module):
    ungrounded = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and not obj.__doc__:
            ungrounded.append(name)
    return ungrounded
```

**Link validation:**
```python
import requests

def validate_links(doc_content):
    links = extract_links(doc_content)
    broken = []
    for link in links:
        try:
            response = requests.head(link, timeout=5)
            if response.status_code >= 400:
                broken.append(link)
        except:
            broken.append(link)
    return broken
```

### 4. Capture Observations

Record:
- Coverage metrics
- Ungrounded claims found
- Broken links or missing evidence

### 5. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Ungrounded claim found | KILLED |
| All claims have support | SURVIVED |
| Can't verify all claims | UNCERTAIN |

## Output Format

```yaml
test:
  method: "Checked test coverage for all assertions"
  code: |
    pytest --cov=src --cov-report=term-missing
observations:
  raw: |
    Overall coverage: 87%
    Uncovered lines in validator.py: 45, 67, 89
    Line 45: assert input is not None
    Line 67: assert len(data) > 0
  unexpected: "Two assertions have no test coverage"
verdict: KILLED
reasoning: "Found 2 assertions without test coverage (ungrounded)"
mutations:
  - "Add tests for validator.py lines 45 and 67"
```

## Grounding Test Patterns

### Test Coverage
```bash
pytest --cov=src --cov-fail-under=100
```

### Doc Coverage
```python
# Using interrogate
interrogate -vv --fail-under=100 src/
```

### Citation Verification
```python
for citation in citations:
    assert citation.url_exists(), f"Citation not found: {citation}"
    assert citation.supports_claim(), f"Citation doesn't support claim"
```

## Tips

1. **Automate checks** — Coverage tools, link checkers
2. **Define "grounded"** — What exactly counts as support?
3. **Check quality** — A test that passes isn't always meaningful
4. **Trace the chain** — Sometimes support is indirect
