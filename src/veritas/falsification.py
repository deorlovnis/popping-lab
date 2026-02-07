"""Falsification engine and testing API for Veritas.

This module provides:
- falsify(): verify a truth against evidence
- quick_check(): convenience for simple cases
- claim(): context manager for inline verification
- verified(): decorator for test functions
- ClaimContext: tracks bindings during a test
"""

from __future__ import annotations

import functools
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Generator, TypeVar

import sympy as sp

from .evidence import Evidence, Verdict, VerdictResult

if TYPE_CHECKING:
    from .truth import FalsificationForm, Truth

F = TypeVar("F", bound=Callable[..., Any])


# ---------------------------------------------------------------------------
# Core falsification
# ---------------------------------------------------------------------------


def _substitute(form: FalsificationForm, evidence: Evidence) -> sp.Basic:
    """Substitute evidence bindings into a falsification form."""
    formula = form.formula
    for symbol, value in evidence.to_sympy().items():
        formula = formula.subs(symbol, value)
    return formula


def _evaluate(substituted: sp.Basic) -> bool | None:
    """Evaluate a substituted formula to a boolean.

    Returns:
        True if the falsification condition is met (claim KILLED).
        False if the condition is not met (claim SURVIVED).
        None if the result cannot be determined.
    """
    simplified = sp.simplify(substituted)

    if simplified is sp.true or simplified == True:  # noqa: E712
        return True
    if simplified is sp.false or simplified == False:  # noqa: E712
        return False

    if hasattr(simplified, 'is_Boolean') and simplified.is_Boolean:
        try:
            return bool(simplified)
        except TypeError:
            pass

    try:
        if isinstance(simplified, sp.Equality):
            lhs_val, rhs_val = simplified.lhs, simplified.rhs
            if not lhs_val.free_symbols and not rhs_val.free_symbols:
                return bool(lhs_val.equals(rhs_val))

        if isinstance(simplified, sp.Ne):
            lhs_val, rhs_val = simplified.lhs, simplified.rhs
            if not lhs_val.free_symbols and not rhs_val.free_symbols:
                return not bool(lhs_val.equals(rhs_val))

        if isinstance(simplified, sp.Rel):
            lhs_val, rhs_val = simplified.lhs, simplified.rhs
            if not lhs_val.free_symbols and not rhs_val.free_symbols:
                return bool(simplified)
    except (TypeError, ValueError, AttributeError):
        pass

    return None


def falsify(truth: Truth, evidence: Evidence) -> VerdictResult:
    """Verify a truth against evidence.

    This is the main entry point. It constructs the falsification form,
    substitutes evidence, evaluates the result, and returns a VerdictResult.

    Args:
        truth: The truth to verify.
        evidence: Evidence to test against.

    Returns:
        VerdictResult with verdict, trace, and reasoning.
    """
    result = VerdictResult(
        verdict=Verdict.UNCERTAIN,
        trace=[],
        reasoning="",
    )

    # Step 1: Get falsification form
    result.add_trace(f"Constructing falsification form for: {truth.statement}")
    form = truth.falsify()
    result.form = form
    result.add_trace(f"Falsification form: {form.description}")

    # Step 2: Check evidence completeness
    result.add_trace(f"Evidence bindings: {evidence.bindings}")
    result.evidence = evidence

    missing = {
        symbol.name
        for symbol in form.free_symbols
        if symbol.name not in evidence.bindings
    }
    if missing:
        result.reasoning = f"Missing evidence for: {missing}"
        result.add_trace(f"Cannot evaluate: missing {missing}")
        return result

    # Step 3: Substitute and evaluate
    substituted = _substitute(form, evidence)
    result.add_trace(f"Substituted formula: {substituted}")

    eval_result = _evaluate(substituted)
    result.add_trace(f"Evaluation result: {eval_result}")

    # Step 4: Determine verdict
    if eval_result is True:
        result.verdict = Verdict.KILLED
        result.reasoning = f"Falsification condition met: {form.description}"
    elif eval_result is False:
        result.verdict = Verdict.SURVIVED
        result.reasoning = "Falsification condition not met with given evidence"
    else:
        result.verdict = Verdict.UNCERTAIN
        result.reasoning = f"Could not evaluate formula: {substituted}"

    return result


def quick_check(truth: Truth, **bindings: Any) -> Verdict:
    """Quick check of a truth with bindings.

    Args:
        truth: The truth to verify.
        **bindings: Variable bindings as keyword arguments.

    Returns:
        Just the Verdict (KILLED, SURVIVED, or UNCERTAIN).
    """
    evidence = Evidence(bindings=bindings)
    return falsify(truth, evidence).verdict


# ---------------------------------------------------------------------------
# Testing API (merged from testing.py)
# ---------------------------------------------------------------------------


@dataclass
class ClaimContext:
    """Context for tracking claims within a test.

    Used by the claim() context manager to collect evidence bindings
    and automatically verify on exit.
    """

    truth: Truth
    """The truth being claimed."""

    evidence: Evidence = field(default_factory=lambda: Evidence(bindings={}))
    """Evidence gathered during the test."""

    result: VerdictResult | None = None
    """The verification result, set on exit."""

    def bind(self, **bindings: Any) -> None:
        """Add bindings to the evidence."""
        self.evidence.bindings.update(bindings)

    def observe(self, name: str, value: Any) -> Any:
        """Observe a value and add it to evidence.

        Returns:
            The value (for chaining).
        """
        self.evidence.bindings[name] = value
        return value


@contextmanager
def claim(truth: Truth) -> Generator[ClaimContext, None, None]:
    """Context manager for testing a claim.

    Example:
        >>> from veritas import Analytic, claim
        >>> def test_addition():
        ...     with claim(Analytic("2+2=4", lhs="result", rhs=4)) as c:
        ...         c.bind(result=2+2)
        ...     assert c.result.verdict == Verdict.SURVIVED

    Yields:
        ClaimContext for adding evidence. Automatically verifies on exit.
    """
    ctx = ClaimContext(truth=truth)
    try:
        yield ctx
    finally:
        ctx.result = falsify(ctx.truth, ctx.evidence)


def verified(truth_factory: Callable[..., Truth]) -> Callable[[F], F]:
    """Decorator to mark a test as verified by Veritas.

    The decorated function should return evidence bindings as a dict.
    The test passes if the claim SURVIVES and fails if KILLED.

    Example:
        >>> @verified(lambda: Analytic("2+2=4", lhs="result", rhs=4))
        ... def test_addition():
        ...     return {"result": 2 + 2}
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> VerdictResult:
            truth = truth_factory()

            bindings = func(*args, **kwargs)

            if bindings is None:
                bindings = {}
            elif not isinstance(bindings, dict):
                bindings = {"result": bindings}

            evidence = Evidence(
                bindings=bindings,
                source=f"test function: {func.__name__}",
            )

            result = falsify(truth, evidence)

            if result.verdict == Verdict.KILLED:
                raise AssertionError(
                    f"Claim KILLED: {truth.statement}\n"
                    f"Reasoning: {result.reasoning}\n"
                    f"Evidence: {evidence.bindings}"
                )

            return result

        return wrapper  # type: ignore

    return decorator
