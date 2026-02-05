"""User-facing testing API for Veritas.

This module provides a pytest-friendly API for using Veritas:
- @verified decorator for test functions
- TestCase protocol for structured tests
- claim() context manager for inline verification
"""

from __future__ import annotations

import functools
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Generator, Protocol, TypeVar

from .engine import Verifier
from .evidence import Evidence, Verdict, VerdictResult
from .truth import Analytic, Empirical, Modal, Probabilistic, Truth

if TYPE_CHECKING:
    pass

F = TypeVar("F", bound=Callable[..., Any])


class TestCase(Protocol):
    """Protocol for a Veritas test case.

    A TestCase provides a structured way to define a test with:
    - A truth to verify
    - A method to gather evidence
    - A method to execute the full test
    """

    @property
    def truth(self) -> Truth:
        """The truth being tested."""
        ...

    def gather_evidence(self) -> Evidence:
        """Gather evidence for verification."""
        ...

    def execute(self) -> VerdictResult:
        """Execute the test and return a result."""
        ...


@dataclass
class ClaimContext:
    """Context for tracking claims within a test.

    Used by the claim() context manager to track what's being tested.
    """

    truth: Truth
    """The truth being claimed."""

    evidence: Evidence = field(default_factory=lambda: Evidence(bindings={}))
    """Evidence gathered during the test."""

    result: VerdictResult | None = None
    """The verification result, set on exit."""

    _verifier: Verifier = field(default_factory=Verifier)
    """The verifier instance."""

    def bind(self, **bindings: Any) -> None:
        """Add bindings to the evidence.

        Args:
            **bindings: Variable name to value mappings
        """
        self.evidence.bindings.update(bindings)

    def observe(self, name: str, value: Any) -> Any:
        """Observe a value and add it to evidence.

        This is useful for capturing intermediate values during a test.

        Args:
            name: Name for this observation
            value: The observed value

        Returns:
            The value (for chaining)
        """
        self.evidence.bindings[name] = value
        return value


@contextmanager
def claim(truth: Truth) -> Generator[ClaimContext, None, None]:
    """Context manager for testing a claim.

    Use this to wrap test code and automatically verify at the end.

    Example:
        >>> from veritas import Analytic, claim
        >>> def test_addition():
        ...     with claim(Analytic("2+2=4", lhs="result", rhs=4)) as c:
        ...         c.bind(result=2+2)
        ...     assert c.result.verdict == Verdict.SURVIVED

    Args:
        truth: The truth to verify

    Yields:
        ClaimContext for adding evidence

    The context automatically verifies on exit and sets c.result.
    """
    ctx = ClaimContext(truth=truth)
    try:
        yield ctx
    finally:
        # Verify on exit
        ctx.result = ctx._verifier.verify(ctx.truth, ctx.evidence)


def verified(truth_factory: Callable[..., Truth]) -> Callable[[F], F]:
    """Decorator to mark a test as verified by Veritas.

    The decorated function should return evidence bindings as a dict.
    The test passes if the claim SURVIVES and fails if KILLED.

    Example:
        >>> @verified(lambda: Analytic("2+2=4", lhs="result", rhs=4))
        ... def test_addition():
        ...     return {"result": 2 + 2}

    Args:
        truth_factory: A callable that returns the Truth to verify

    Returns:
        Decorator that wraps the test function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> VerdictResult:
            truth = truth_factory()
            verifier = Verifier()

            # Execute the test function
            bindings = func(*args, **kwargs)

            # Handle different return types
            if bindings is None:
                bindings = {}
            elif not isinstance(bindings, dict):
                # If a single value is returned, use "result" as the key
                bindings = {"result": bindings}

            evidence = Evidence(
                bindings=bindings,
                source=f"test function: {func.__name__}",
            )

            result = verifier.verify(truth, evidence)

            # Raise assertion error if KILLED
            if result.verdict == Verdict.KILLED:
                raise AssertionError(
                    f"Claim KILLED: {truth.statement}\n"
                    f"Reasoning: {result.reasoning}\n"
                    f"Evidence: {evidence.bindings}"
                )

            # Warn on UNCERTAIN if strict
            if result.verdict == Verdict.UNCERTAIN and verifier.strict:
                raise AssertionError(
                    f"Claim UNCERTAIN: {truth.statement}\n"
                    f"Reasoning: {result.reasoning}"
                )

            return result

        return wrapper  # type: ignore

    return decorator


# Builder functions for common patterns


def equality(
    statement: str,
    lhs: str = "result",
    rhs: Any = None,
    var_name: str = "x",
) -> Analytic:
    """Build an equality claim.

    Convenience function for creating Analytic truths.

    Args:
        statement: Human-readable claim
        lhs: Variable name for the computed value
        rhs: Expected value
        var_name: Variable name for the free variable

    Returns:
        An Analytic truth
    """
    return Analytic(
        statement=statement,
        lhs=lhs,
        rhs=rhs,
        var_name=var_name,
    )


def invariant(
    statement: str,
    predicate: Any,
    state_var: str = "state",
) -> Modal:
    """Build an invariant claim.

    Convenience function for creating Modal truths.

    Args:
        statement: Human-readable claim
        predicate: The property that must hold
        state_var: Variable name for the state

    Returns:
        A Modal truth
    """
    return Modal(
        statement=statement,
        invariant=predicate,
        state_var=state_var,
    )


def empirical(
    statement: str,
    observation_var: str = "obs",
    expected: Callable[[Any], bool] | None = None,
    contradiction: str = "",
) -> Empirical:
    """Build an empirical claim.

    Convenience function for creating Empirical truths.

    Args:
        statement: Human-readable claim
        observation_var: Variable name for observations
        expected: Predicate that observations should satisfy
        contradiction: Description of what contradicts the claim

    Returns:
        An Empirical truth
    """
    return Empirical(
        statement=statement,
        observation_var=observation_var,
        expected_predicate=expected,
        contradiction_description=contradiction,
    )


def probabilistic(
    statement: str,
    metric: str = "p",
    threshold: float = 0.5,
    direction: str = ">",
) -> Probabilistic:
    """Build a probabilistic claim.

    Convenience function for creating Probabilistic truths.

    Args:
        statement: Human-readable claim
        metric: Name of the metric
        threshold: The threshold value
        direction: Comparison direction ('>', '>=', '<', '<=', '=')

    Returns:
        A Probabilistic truth
    """
    return Probabilistic(
        statement=statement,
        metric=metric,
        threshold=threshold,
        direction=direction,
    )
