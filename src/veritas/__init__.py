"""Veritas: SymPy-verified falsification for claims.

Veritas provides a formal framework for testing claims against evidence.
Claims are represented as Truth types, each with a specific falsification form.

## Truth Types

- **Analytic**: Equality claims (∃x: f(x) ≠ y)
- **Modal**: Necessity claims (◇¬P, invariant violation)
- **Empirical**: Observation-based claims
- **Probabilistic**: Threshold-based claims (P(X) ≤ t)

## Quick Start

```python
from veritas import Analytic, Evidence, falsify

# Define a truth
truth = Analytic(
    statement="add(2, 2) equals 4",
    lhs="result",
    rhs=4,
)

# Gather evidence
evidence = Evidence(bindings={"result": 4})

# Verify
result = falsify(truth, evidence)
print(result.verdict)  # SURVIVED
```

## Testing API

```python
from veritas import claim, Analytic

def test_addition():
    with claim(Analytic("2+2=4", lhs="result", rhs=4)) as c:
        c.bind(result=2+2)
    assert c.result.verdict.name == "SURVIVED"
```
"""

from .evidence import Evidence, Verdict, VerdictResult
from .extensions import (
    DataGrounding,
    DomainTruth,
    HTTPResponse,
    InvariantCheck,
    ModelAccuracy,
)
from .falsification import ClaimContext, claim, falsify, quick_check, verified
from .truth import Analytic, Empirical, FalsificationForm, Modal, Probabilistic, Truth

__all__ = [
    # Truth types
    "Truth",
    "FalsificationForm",
    "Analytic",
    "Modal",
    "Empirical",
    "Probabilistic",
    # Evidence & verdicts
    "Evidence",
    "Verdict",
    "VerdictResult",
    # Falsification
    "falsify",
    "quick_check",
    # Testing API
    "claim",
    "verified",
    "ClaimContext",
    # Extensions
    "DomainTruth",
    "HTTPResponse",
    "ModelAccuracy",
    "InvariantCheck",
    "DataGrounding",
]

__version__ = "0.1.0"
