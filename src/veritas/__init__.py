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
from veritas import Analytic, Evidence, verify

# Define a truth
truth = Analytic(
    statement="add(2, 2) equals 4",
    lhs="result",
    rhs=4,
)

# Gather evidence
evidence = Evidence(bindings={"result": 4})

# Verify
result = verify(truth, evidence)
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

from .engine import Verifier, quick_check, verify
from .evidence import Evidence, Verdict, VerdictResult
from .extensions import (
    DataGrounding,
    DomainTruth,
    HTTPResponse,
    InvariantCheck,
    ModelAccuracy,
)
from .testing import (
    ClaimContext,
    claim,
    empirical,
    equality,
    invariant,
    probabilistic,
    verified,
)
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
    # Engine
    "Verifier",
    "verify",
    "quick_check",
    # Testing API
    "claim",
    "verified",
    "ClaimContext",
    "equality",
    "invariant",
    "empirical",
    "probabilistic",
    # Extensions
    "DomainTruth",
    "HTTPResponse",
    "ModelAccuracy",
    "InvariantCheck",
    "DataGrounding",
]

__version__ = "0.1.0"
