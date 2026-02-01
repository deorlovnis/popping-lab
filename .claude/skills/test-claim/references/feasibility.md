# Testing Feasibility Claims

Feasibility claims require building something to test if X can work.

Kill target: **Show blocker that prevents X from working**

## Methodology

### 1. Build Minimal POC

Use the `build-poc` skill to create the smallest working prototype.

- Focus on core mechanism only
- Skip UI unless UI is the claim
- Use existing libraries/APIs where possible
- Time-box: hours, not days

### 2. Design the Test

What specific action will test the claim?

| Claim Type | Test Approach |
|------------|---------------|
| "Can detect X" | Collect samples, run detection, measure accuracy |
| "Can predict X" | Split data, train/test, compare to baseline |
| "Can build X" | Build it, measure if it works |
| "X is faster" | Benchmark both, compare |

### 3. Execute and Observe

Run the POC and capture:
- Exact output/results
- Error messages
- Performance metrics
- Blockers encountered
- Unexpected behaviors

### 4. Identify Blockers

What could prove infeasibility?
- Missing required data/API
- Fundamental limitation (laws of physics, math)
- Resource constraints (compute, memory, time)
- Accuracy below baseline/random

### 5. Compare to Kill Criteria

Go through each criterion:
- Is blocker found? → KILLED
- All criteria unmet? → SURVIVED
- Can't determine? → UNCERTAIN

## Output Format

```yaml
test:
  method: "Built POC to test if typing patterns predict stress"
  code: |
    import numpy as np
    from sklearn.linear_model import LogisticRegression

    # Collect typing metrics
    X = extract_features(typing_samples)
    y = stress_labels

    # Train and evaluate
    model = LogisticRegression()
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    print(f"Accuracy: {accuracy:.2%}")
observations:
  raw: |
    Trained on 500 samples
    Test accuracy: 58%
    Baseline (random): 50%
  unexpected: "Signal exists but weak"
verdict: SURVIVED
reasoning: "Accuracy 58% > 50% baseline. Signal exists, claim is feasible."
mutations:
  - "With more data, accuracy might improve"
  - "Feature engineering could strengthen signal"
```

## Feasibility Test Patterns

### Accuracy vs Baseline
```python
accuracy = evaluate(model, test_data)
baseline = 1.0 / num_classes  # Random chance
assert accuracy > baseline, f"No better than random: {accuracy}"
```

### API Availability
```python
def test_api_exists():
    try:
        response = requests.get(API_ENDPOINT)
        assert response.status_code == 200
    except Exception as e:
        raise AssertionError(f"BLOCKER: API unavailable - {e}")
```

### Resource Feasibility
```python
import time

start = time.time()
result = heavy_computation()
elapsed = time.time() - start

assert elapsed < MAX_ACCEPTABLE_TIME, f"BLOCKER: Takes {elapsed}s, max is {MAX_ACCEPTABLE_TIME}s"
```

## Common Blockers

| Blocker | Example |
|---------|---------|
| Data unavailable | API deprecated, no training data |
| Below baseline | Accuracy ≤ random chance |
| Resource constraint | Takes days to run, needs GPU |
| Fundamental limit | Violates physics/math |
| External dependency | Required service doesn't exist |

## Tips

1. **POC, not product** — Test the mechanism, not polish
2. **Document blockers** — Why exactly can't it work?
3. **Be honest** — "Works" needs quantification
4. **Capture surprises** — Unexpected findings are valuable
5. **Time-box** — If POC takes too long, scope is too big
