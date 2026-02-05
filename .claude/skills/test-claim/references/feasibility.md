# Testing Feasibility Claims → Empirical/Probabilistic Verification

Feasibility claims are tested using **Empirical** (blockers) or **Probabilistic** (thresholds) truths in Veritas.

**Kill targets:**
- Empirical: Find blocker that prevents X from working
- Probabilistic: Metric fails to meet threshold

## Methodology

### 1. Build Minimal POC

Use the `build-poc` skill to create the smallest working prototype.

- Focus on core mechanism only
- Skip UI unless UI is the claim
- Use existing libraries/APIs where possible
- Time-box: hours, not days

### 2. Design the Test

What specific action will test the claim?

| Claim Type | Test Approach | Veritas Truth |
|------------|---------------|---------------|
| "Can detect X" | Collect samples, run detection | Probabilistic |
| "Can predict X" | Split data, train/test | Probabilistic |
| "Can build X" | Build it, check for blockers | Empirical |
| "X is faster" | Benchmark both, compare | Probabilistic |

### 3. Execute with Veritas

**For Blocker Detection:**

```python
from veritas import Empirical, Verifier

truth = Empirical(
    statement="Can build typing-based stress predictor",
    observation_var="blocker",
    expected_predicate=lambda x: x is None,  # No blocker
    contradiction_description="Found blocker",
)

def build_poc():
    # Attempt to build core mechanism
    try:
        # Check data availability
        if not has_typing_data():
            return "BLOCKER: No typing data available"

        # Check API availability
        if not api_accessible():
            return "BLOCKER: Required API not accessible"

        # Check computational feasibility
        if training_time > MAX_TIME:
            return f"BLOCKER: Training takes {training_time}s, max is {MAX_TIME}s"

        return None  # No blocker
    except Exception as e:
        return f"BLOCKER: {e}"

blocker = build_poc()

verifier = Verifier()
result = verifier.verify_with_predicate(truth, blocker, "check_observation")

if result.is_killed():
    print(f"Infeasible: {blocker}")
else:
    print("Feasible: No blockers found")
```

**For Threshold Testing:**

```python
from veritas import Probabilistic, Verifier, Evidence

truth = Probabilistic(
    statement="Model accuracy > 60%",
    metric="accuracy",
    threshold=0.6,
    direction=">",
)

# Build and evaluate POC
model = build_minimal_model()
accuracy = evaluate(model, test_data)

# Verify threshold
result = Verifier().verify_with_predicate(
    truth, accuracy, "check_threshold"
)

if result.is_survived():
    print(f"Feasible: accuracy={accuracy:.2%}")
else:
    print(f"Infeasible: accuracy={accuracy:.2%} < 60%")
```

### 4. Compare to Baseline

```python
from veritas import Probabilistic, Verifier

truth = Probabilistic(
    statement="Semantic search > keyword search",
    metric="improvement",
    threshold=0.0,  # > 0 means improvement
    direction=">",
)

# Run both approaches
keyword_score = run_keyword_search(queries, corpus)
semantic_score = run_semantic_search(queries, corpus)

improvement = (semantic_score - keyword_score) / keyword_score

result = Verifier().verify_with_predicate(
    truth, improvement, "check_threshold"
)

if result.is_survived():
    print(f"Semantic search is {improvement:.1%} better")
else:
    print(f"Semantic search is NOT better (improvement={improvement:.1%})")
```

### 5. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Blocker found | KILLED |
| Below baseline | KILLED |
| Threshold not met | KILLED |
| POC works, threshold met | SURVIVED |
| Can't complete POC | UNCERTAIN |

## Common Blockers

| Blocker Type | How to Detect | Veritas Pattern |
|--------------|---------------|-----------------|
| Data unavailable | API check, file check | Empirical |
| Below baseline | Compare metrics | Probabilistic |
| Resource constraint | Measure time/memory | Empirical or Probabilistic |
| Fundamental limit | Domain knowledge | Empirical |
| External dependency | Service check | Empirical |

## Testing Patterns

### API Availability

```python
from veritas import Empirical, Verifier
import requests

truth = Empirical(
    statement="Required API is accessible",
    observation_var="blocker",
    expected_predicate=lambda x: x is None,
)

def check_api():
    try:
        response = requests.get(API_ENDPOINT, timeout=5)
        if response.status_code != 200:
            return f"BLOCKER: API returned {response.status_code}"
        return None
    except Exception as e:
        return f"BLOCKER: API unavailable - {e}"

blocker = check_api()
result = Verifier().verify_with_predicate(truth, blocker, "check_observation")
```

### Resource Feasibility

```python
from veritas import Probabilistic, Verifier
import time

truth = Probabilistic(
    statement="Computation completes in < 60s",
    metric="time",
    threshold=60,
    direction="<",
)

start = time.time()
result = heavy_computation()
elapsed = time.time() - start

verdict = Verifier().verify_with_predicate(truth, elapsed, "check_threshold")

if verdict.is_killed():
    print(f"BLOCKER: Takes {elapsed}s, max is 60s")
```

### Accuracy vs Random

```python
from veritas import Probabilistic, Verifier

num_classes = 2
random_baseline = 1.0 / num_classes

truth = Probabilistic(
    statement="Model better than random",
    metric="accuracy",
    threshold=random_baseline,
    direction=">",
)

accuracy = evaluate(model, test_data)

result = Verifier().verify_with_predicate(truth, accuracy, "check_threshold")

if result.is_killed():
    print(f"KILLED: accuracy={accuracy:.2%} <= random={random_baseline:.2%}")
```

## Tips

1. **POC, not product** — Test the mechanism, not polish
2. **Document blockers** — Why exactly can't it work?
3. **Be honest** — "Works" needs quantification
4. **Capture surprises** — Unexpected findings are valuable
5. **Time-box** — If POC takes too long, scope is too big
