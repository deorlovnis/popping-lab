# Testing Ordering Claims → Analytic Verification

Ordering claims are tested using **Analytic** truths in Veritas.

**Kill target:** ∃i: order(seq[i], seq[i+1]) violated

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

### 3. Execute with Veritas

```python
from veritas import claim, Analytic, Verdict

# Define ordering as equality check on sorted property
truth = Analytic(
    statement="list is sorted ascending",
    lhs="is_sorted",
    rhs=True,
)

def check_sorted(seq):
    return all(seq[i] <= seq[i+1] for i in range(len(seq)-1))

with claim(truth) as c:
    data = get_sorted_results()
    c.bind(is_sorted=check_sorted(data), x=check_sorted(data))

print(c.result.verdict)
```

### 4. Render Verdict

| Scenario | Verdict |
|----------|---------|
| Order violation found | KILLED |
| Order maintained in all tests | SURVIVED |
| Couldn't test thoroughly | UNCERTAIN |

## Testing Patterns

### Sort Verification

```python
from veritas import claim, Analytic

truth = Analytic(
    statement="search results sorted by relevance descending",
    lhs="is_sorted",
    rhs=True,
)

with claim(truth) as c:
    results = search("query")
    is_sorted = all(
        results[i].score >= results[i+1].score
        for i in range(len(results)-1)
    )
    c.bind(is_sorted=is_sorted, x=is_sorted)

if c.result.is_killed():
    print("Sort order violated!")
```

### Priority Queue

```python
from veritas import claim, Analytic

truth = Analytic(
    statement="priority queue maintains order",
    lhs="order_correct",
    rhs=True,
)

def test_priority_queue():
    queue = PriorityQueue()
    for item in items:
        queue.insert(item)

    dequeued = []
    while not queue.empty():
        dequeued.append(queue.pop())

    # Check order
    order_correct = all(
        dequeued[i].priority <= dequeued[i+1].priority
        for i in range(len(dequeued)-1)
    )

    with claim(truth) as c:
        c.bind(order_correct=order_correct, x=order_correct)

    return c.result
```

### Transitivity Check

```python
from veritas import claim, Analytic
from hypothesis import given, strategies as st

truth = Analytic(
    statement="ordering is transitive",
    lhs="transitive",
    rhs=True,
)

@given(st.lists(st.integers(), min_size=3))
def test_transitivity(items):
    a, b, c = items[:3]

    # If a <= b and b <= c, then a <= c
    if a <= b and b <= c:
        transitive = a <= c
    else:
        transitive = True  # Precondition not met

    with claim(truth) as ctx:
        ctx.bind(transitive=transitive, x=transitive)

    assert ctx.result.verdict != Verdict.KILLED
```

### Stability Test

```python
from veritas import claim, Analytic

truth = Analytic(
    statement="sort is stable for equal keys",
    lhs="is_stable",
    rhs=True,
)

def test_sort_stability():
    # Items with same key should maintain original order
    items = [(1, 'a'), (2, 'b'), (1, 'c')]
    sorted_items = stable_sort_by_key(items)

    # Find items with key=1 and check original order preserved
    ones = [item for item in sorted_items if item[0] == 1]
    is_stable = ones == [(1, 'a'), (1, 'c')]

    with claim(truth) as c:
        c.bind(is_stable=is_stable, x=is_stable)

    return c.result
```

### Heap Property

```python
from veritas import claim, Analytic

truth = Analytic(
    statement="heap property maintained",
    lhs="is_heap",
    rhs=True,
)

def verify_heap(arr):
    """Check min-heap property: parent <= children"""
    for i in range(len(arr)):
        left = 2*i + 1
        right = 2*i + 2
        if left < len(arr) and arr[i] > arr[left]:
            return False
        if right < len(arr) and arr[i] > arr[right]:
            return False
    return True

with claim(truth) as c:
    heap = build_heap(data)
    c.bind(is_heap=verify_heap(heap), x=verify_heap(heap))
```

## Tips

1. **Test after mutations** — Order can break after insert/delete
2. **Check stability** — What happens with equal elements?
3. **Verify transitivity** — a<b, b<c implies a<c
4. **Random testing** — Property testing finds edge cases
