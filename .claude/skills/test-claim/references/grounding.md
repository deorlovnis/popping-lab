# Testing Grounding Claims → Empirical Verification

Grounding claims are tested using **Empirical** truths in Veritas.

**Kill target:** Find observation that contradicts claimed support

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

### 3. Execute with Veritas

```python
from veritas import Empirical, Verifier

# Define grounding claim
truth = Empirical(
    statement="All public methods have docstrings",
    observation_var="undocumented",
    expected_predicate=lambda x: x is None,  # No undocumented methods
    contradiction_description="Found public method without docstring",
)

# Check the codebase
def find_undocumented_methods(module):
    import inspect
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and not name.startswith('_'):
            if not obj.__doc__:
                return name
    return None

undocumented = find_undocumented_methods(my_module)

# Use Verifier directly for Empirical predicates
verifier = Verifier()
result = verifier.verify_with_predicate(
    truth, undocumented, "check_observation"
)

if result.is_killed():
    print(f"Grounding broken: {undocumented} has no docstring")
```

### 4. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Ungrounded claim found | KILLED |
| All claims have support | SURVIVED |
| Can't verify all claims | UNCERTAIN |

## Testing Patterns

### Test Coverage

```python
from veritas import Empirical, Verifier
import subprocess

truth = Empirical(
    statement="All assertions have test coverage",
    observation_var="uncovered",
    expected_predicate=lambda x: x is None or len(x) == 0,
    contradiction_description="Found uncovered assertions",
)

# Run coverage analysis
result = subprocess.run(
    ["pytest", "--cov=src", "--cov-report=term-missing"],
    capture_output=True,
    text=True
)

# Parse for uncovered lines containing 'assert'
uncovered_asserts = parse_uncovered_asserts(result.stdout)

verifier = Verifier()
verdict = verifier.verify_with_predicate(
    truth, uncovered_asserts, "check_observation"
)

if verdict.is_killed():
    print(f"Ungrounded assertions: {uncovered_asserts}")
```

### Documentation Coverage

```python
from veritas import Empirical, Verifier
import ast
import inspect

truth = Empirical(
    statement="All public functions documented",
    observation_var="undocumented",
    expected_predicate=lambda x: x is None,
    contradiction_description="Found undocumented function",
)

def check_docstrings(module_path):
    with open(module_path) as f:
        tree = ast.parse(f.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith('_'):
                if not ast.get_docstring(node):
                    return node.name
    return None

undocumented = check_docstrings("src/mymodule.py")

verifier = Verifier()
result = verifier.verify_with_predicate(truth, undocumented, "check_observation")
```

### Link Validation

```python
from veritas import Empirical, Verifier
import requests
import re

truth = Empirical(
    statement="All documentation links are valid",
    observation_var="broken_link",
    expected_predicate=lambda x: x is None,
    contradiction_description="Found broken link",
)

def validate_links(doc_content):
    url_pattern = r'https?://[^\s\)\]>]+'
    links = re.findall(url_pattern, doc_content)

    for link in links:
        try:
            response = requests.head(link, timeout=5, allow_redirects=True)
            if response.status_code >= 400:
                return link
        except requests.RequestException:
            return link
    return None

with open("README.md") as f:
    broken = validate_links(f.read())

verifier = Verifier()
result = verifier.verify_with_predicate(truth, broken, "check_observation")
```

### Citation Verification

```python
from veritas import Empirical, Verifier

truth = Empirical(
    statement="All citations exist and are accessible",
    observation_var="invalid_citation",
    expected_predicate=lambda x: x is None,
    contradiction_description="Found invalid citation",
)

def verify_citations(citations):
    for citation in citations:
        if not citation_exists(citation):
            return citation
        if not citation_supports_claim(citation):
            return citation
    return None

invalid = verify_citations(paper_citations)

verifier = Verifier()
result = verifier.verify_with_predicate(truth, invalid, "check_observation")
```

## Tips

1. **Automate checks** — Coverage tools, link checkers
2. **Define "grounded"** — What exactly counts as support?
3. **Check quality** — A test that passes isn't always meaningful
4. **Trace the chain** — Sometimes support is indirect
