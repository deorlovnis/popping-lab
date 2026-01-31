# Testing Belief Claims

Belief claims require gathering evidence, not running code.

## Methodology

### 1. Identify Evidence Sources

Where could supporting/refuting evidence exist?

| Belief Type | Evidence Sources |
|-------------|------------------|
| Performance | Metrics dashboards, APM, logs |
| User behavior | Analytics, heatmaps, surveys |
| Code quality | Static analysis, coverage reports |
| Assumptions | Documentation, git history, Slack |

### 2. Design the Test

What specific evidence would prove/disprove the belief?

**Example belief:** "Caching improves latency by 40%"

Evidence needed:
- Latency before caching (baseline)
- Latency after caching (current)
- Sample size for statistical validity
- Same conditions (load, data, hardware)

### 3. Gather Evidence

**From metrics:**
```python
# Query prometheus/datadog/etc
before_p95 = query_metric("http_latency_p95", time_range="before_cache")
after_p95 = query_metric("http_latency_p95", time_range="after_cache")

improvement = (before_p95 - after_p95) / before_p95 * 100
print(f"Improvement: {improvement:.1f}%")
```

**From logs:**
```bash
# Extract timing data from logs
grep "request_duration" app.log | awk '{sum+=$3; count++} END {print sum/count}'
```

**From code analysis:**
```python
# Check if claim matches implementation
# Read the code, look for evidence
```

**From web search:**
- Find benchmarks, studies, documentation
- Look for contradicting evidence
- Check if assumptions are outdated

### 4. Evaluate Evidence Quality

Consider:
- **Sample size** — Is this statistically meaningful?
- **Recency** — Is this data current?
- **Conditions** — Same environment?
- **Bias** — What might skew results?

### 5. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Clear evidence contradicts claim | KILLED |
| Evidence supports claim, good quality | SURVIVED |
| Evidence is weak, conflicting, or unavailable | UNCERTAIN |

## Output Format

```yaml
test:
  method: "Queried latency metrics before/after caching implementation"
  code: |
    # Evidence gathering approach
    before = get_p95_latency("2024-01-01", "2024-01-15")
    after = get_p95_latency("2024-01-16", "2024-01-31")
observations:
  raw: |
    Before caching: p95 = 450ms (n=10,000 requests)
    After caching: p95 = 290ms (n=12,000 requests)
    Improvement: 35.5%
  unexpected: "Cache hit rate only 60%, room for improvement"
verdict: KILLED
reasoning: "Claim was >40% improvement. Observed 35.5%. Close but criterion not met."
mutations:
  - "Caching improves latency by ~35% at 60% cache hit rate"
  - "Improving cache hit rate could reach 40% target"
```

## Evidence Gathering Tips

1. **Seek disconfirmation** — Actively look for evidence against
2. **Check the source** — Who measured this? When? How?
3. **Compare like to like** — Same conditions?
4. **Quantify uncertainty** — Confidence intervals if possible
5. **Document gaps** — What evidence couldn't you find?

## When Evidence Is Unavailable

If you can't find evidence:
1. Can you generate it? (Run a benchmark)
2. Can you find proxy evidence?
3. Should this become a SPARK claim instead?

UNCERTAIN is valid when evidence is genuinely lacking.
