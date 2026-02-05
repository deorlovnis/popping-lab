"""Evidence and verdict data structures for Veritas.

This module defines:
- Evidence: concrete bindings for symbolic variables
- Verdict: the possible outcomes of falsification
- VerdictResult: the complete result of a verification
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

import sympy as sp

from .symbolic import sym

if TYPE_CHECKING:
    from .truth import FalsificationForm


class Verdict(Enum):
    """The outcome of a falsification attempt.

    KILLED: Falsification criteria met - claim is false
    SURVIVED: Criteria not met, test was valid - claim held up
    UNCERTAIN: Inconclusive - test was flawed or blocked
    """

    KILLED = "KILLED"
    SURVIVED = "SURVIVED"
    UNCERTAIN = "UNCERTAIN"

    def __str__(self) -> str:
        return self.value


@dataclass
class Evidence:
    """Concrete evidence for falsification.

    Evidence provides bindings from symbolic variables to concrete values,
    along with metadata about how the evidence was gathered.

    Example:
        >>> e = Evidence(
        ...     bindings={"x": 5, "result": 25},
        ...     source="pytest execution",
        ...     metadata={"test_file": "test_math.py"}
        ... )
    """

    bindings: dict[str, Any]
    """Variable name to concrete value mappings."""

    source: str = ""
    """Description of how evidence was gathered."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata about the evidence."""

    def to_sympy(self) -> dict[sp.Symbol, Any]:
        """Convert bindings to SymPy symbol mappings.

        Returns:
            Dict mapping SymPy Symbols to their bound values.
        """
        return {sym(name): value for name, value in self.bindings.items()}

    def get(self, name: str, default: Any = None) -> Any:
        """Get a binding value by name.

        Args:
            name: Variable name
            default: Default if not found

        Returns:
            The bound value or default.
        """
        return self.bindings.get(name, default)

    def __contains__(self, name: str) -> bool:
        """Check if a variable is bound."""
        return name in self.bindings


@dataclass
class VerdictResult:
    """The complete result of a verification attempt.

    A VerdictResult captures everything about a falsification attempt:
    - The verdict (KILLED, SURVIVED, UNCERTAIN)
    - The falsification form that was tested
    - The evidence used
    - The reasoning trace
    """

    verdict: Verdict
    """The outcome of the verification."""

    form: FalsificationForm | None = None
    """The falsification form that was evaluated."""

    evidence: Evidence | None = None
    """The evidence that was gathered."""

    trace: list[str] = field(default_factory=list)
    """Step-by-step trace of the verification process."""

    reasoning: str = ""
    """Human-readable explanation of why this verdict was reached."""

    mutations: list[str] = field(default_factory=list)
    """New claims that emerged from this test."""

    def is_killed(self) -> bool:
        """Check if the claim was killed."""
        return self.verdict == Verdict.KILLED

    def is_survived(self) -> bool:
        """Check if the claim survived."""
        return self.verdict == Verdict.SURVIVED

    def is_uncertain(self) -> bool:
        """Check if the result is uncertain."""
        return self.verdict == Verdict.UNCERTAIN

    def add_trace(self, step: str) -> None:
        """Add a step to the trace."""
        self.trace.append(step)

    def add_mutation(self, mutation: str) -> None:
        """Add a mutation (new claim) that emerged."""
        self.mutations.append(mutation)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization.

        Returns:
            Dictionary representation of the result.
        """
        return {
            "verdict": str(self.verdict),
            "reasoning": self.reasoning,
            "trace": self.trace,
            "mutations": self.mutations,
            "evidence": self.evidence.bindings if self.evidence else None,
            "form_description": self.form.description if self.form else None,
        }

    def __str__(self) -> str:
        """Human-readable string representation."""
        lines = [f"Verdict: {self.verdict}"]
        if self.reasoning:
            lines.append(f"Reasoning: {self.reasoning}")
        if self.evidence and self.evidence.bindings:
            lines.append(f"Evidence: {self.evidence.bindings}")
        if self.mutations:
            lines.append(f"Mutations: {self.mutations}")
        return "\n".join(lines)
