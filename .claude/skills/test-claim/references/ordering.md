# Testing Ordering Claims

Ordering claims test that comparison relationships are maintained.

Kill target: **Find order violation (X > Y when X ≤ Y expected)**

## Methodology

### 1. Identify the Ordering

What relationship must hold?
- Ascending sort: a[i] <= a[i+1]
- Priority queue: parent <= children
- FIFO: dequeue order = enqueue order
- Ranking: higher score = earlier position

### 2. Design Test Cases

Where might order be violated?
- After insertions
- After deletions
- After updates
- With equal elements (stability)
- Under concurrent access

### 3. Execute Tests

**Sort verification:**
```python
def test_sorted():
    data = get_sorted_results()
    for i in range(len(data) - 1):
        assert data[i] <= data[i+1], f"Order violated at {i}: {data[i]} > {data[i+1]}"
```

**Priority queue:**
```python
def test_priority_order():
    queue = PriorityQueue()
    for item in items:
        queue.insert(item)

    prev = queue.pop()
    while not queue.empty():
        curr = queue.pop()
        assert prev.priority <= curr.priority, f"Order violated: {prev} after {curr}"
        prev = curr
```

**Transitivity check:**
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers(), min_size=3))
def test_transitivity(items):
    a, b, c = items[:3]
    if compare(a, b) <= 0 and compare(b, c) <= 0:
        assert compare(a, c) <= 0, "Transitivity violated"
```

### 4. Capture Observations

Record:
- Any order violations found
- Behavior with equal elements
- Edge cases (empty, single element)

### 5. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Order violation found | KILLED |
| Order maintained in all tests | SURVIVED |
| Couldn't test thoroughly | UNCERTAIN |

## Output Format

```yaml
test:
  method: "Verified search results sorted by relevance descending"
  code: |
    results = search("query")
    for i in range(len(results) - 1):
        assert results[i].score >= results[i+1].score
observations:
  raw: |
    10 results returned
    Scores: [0.95, 0.87, 0.82, 0.79, 0.65, 0.60, 0.58, 0.45, 0.32, 0.21]
    Order verified: True
  unexpected: "None"
verdict: SURVIVED
reasoning: "All adjacent pairs satisfy score[i] >= score[i+1]"
```

## Ordering Test Patterns

### Pairwise Comparison
```python
for i in range(len(seq) - 1):
    assert seq[i] <= seq[i + 1]
```

### Stability Test
```python
# Equal elements should maintain original order
items = [(1, 'a'), (2, 'b'), (1, 'c')]
sorted_items = sort_by_key(items)
assert sorted_items == [(1, 'a'), (1, 'c'), (2, 'b')]  # Stable
```

### Heap Property
```python
def verify_heap(arr, i=0):
    left = 2*i + 1
    right = 2*i + 2
    if left < len(arr):
        assert arr[i] <= arr[left]
        verify_heap(arr, left)
    if right < len(arr):
        assert arr[i] <= arr[right]
        verify_heap(arr, right)
```

## Tips

1. **Test after mutations** — Order can break after insert/delete
2. **Check stability** — What happens with equal elements?
3. **Verify transitivity** — a<b, b<c implies a<c
4. **Random testing** — Property testing finds edge cases
