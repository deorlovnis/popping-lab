"""Verification engine for Veritas falsification.

This module provides the core verification logic:
- Substitute: bind evidence into formulas
- Evaluate: determine boolean truth of substituted formulas
- Verify: complete verification returning a VerdictResult
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import sympy as sp

from .evidence import Evidence, Verdict, VerdictResult
from .symbolic import sym

if TYPE_CHECKING:
    from .truth import FalsificationForm, Truth


class Verifier:
    """Engine for verifying truths against evidence.

    The Verifier takes a Truth and Evidence, constructs the falsification
    form, substitutes evidence, and determines a verdict.

    Example:
        >>> from veritas import Analytic, Evidence, Verifier
        >>> truth = Analytic("2+2=4", lhs="result", rhs=4)
        >>> evidence = Evidence(bindings={"result": 4})
        >>> verifier = Verifier()
        >>> result = verifier.verify(truth, evidence)
        >>> print(result.verdict)
        SURVIVED
    """

    def __init__(self, strict: bool = False) -> None:
        """Initialize the verifier.

        Args:
            strict: If True, UNCERTAIN verdicts are treated as failures
        """
        self.strict = strict

    def substitute(
        self, form: FalsificationForm, evidence: Evidence
    ) -> sp.Basic:
        """Substitute evidence bindings into a falsification form.

        Args:
            form: The falsification form with free symbols
            evidence: Evidence providing concrete bindings

        Returns:
            The formula with evidence substituted in.
        """
        formula = form.formula
        sympy_bindings = evidence.to_sympy()

        for symbol, value in sympy_bindings.items():
            formula = formula.subs(symbol, value)

        return formula

    def evaluate(self, substituted: sp.Basic) -> bool | None:
        """Evaluate a substituted formula to a boolean.

        Args:
            substituted: Formula with concrete values substituted

        Returns:
            True if the formula evaluates to True (falsification succeeded)
            False if the formula evaluates to False
            None if cannot be determined
        """
        # Try to simplify to a boolean
        simplified = sp.simplify(substituted)

        # Check for explicit boolean values
        if simplified is sp.true or simplified == True:  # noqa: E712
            return True
        if simplified is sp.false or simplified == False:  # noqa: E712
            return False

        # Check for Python bool wrapped in SymPy
        if hasattr(sp, 'Boolean') and isinstance(simplified, sp.Boolean):
            try:
                return bool(simplified)
            except TypeError:
                pass
        # Also check for BooleanAtom (True/False in SymPy)
        if hasattr(simplified, 'is_Boolean') and simplified.is_Boolean:
            try:
                return bool(simplified)
            except TypeError:
                pass

        # Try to evaluate numerically if possible
        try:
            # For equality checks
            if isinstance(simplified, sp.Equality):
                lhs_val = simplified.lhs
                rhs_val = simplified.rhs
                # If both sides are concrete values (not symbols)
                if not lhs_val.free_symbols and not rhs_val.free_symbols:
                    return bool(lhs_val.equals(rhs_val))

            # For inequality checks (Ne)
            if isinstance(simplified, sp.Ne):
                lhs_val = simplified.lhs
                rhs_val = simplified.rhs
                if not lhs_val.free_symbols and not rhs_val.free_symbols:
                    return not bool(lhs_val.equals(rhs_val))

            # For relational comparisons
            if isinstance(simplified, sp.Rel):
                lhs_val = simplified.lhs
                rhs_val = simplified.rhs
                if not lhs_val.free_symbols and not rhs_val.free_symbols:
                    return bool(simplified)
        except (TypeError, ValueError, AttributeError):
            pass

        # Cannot determine
        return None

    def _evaluate_falsification_directly(
        self, truth: Any, evidence: Evidence
    ) -> bool | None:
        """Directly evaluate falsification without going through symbolic formulas.

        For Analytic truths, we check if lhs != rhs.
        This bypasses SymPy quantifier issues.

        Args:
            truth: The truth being verified
            evidence: Evidence with bindings

        Returns:
            True if falsification condition is met (claim KILLED)
            False if not met (claim SURVIVED)
            None if cannot determine
        """
        from .truth import Analytic, Modal

        if isinstance(truth, Analytic):
            # Get the actual value from evidence
            lhs_name = truth.lhs if isinstance(truth.lhs, str) else str(truth.lhs)
            if lhs_name in evidence.bindings:
                actual = evidence.bindings[lhs_name]
                expected = truth.rhs
                # Falsification: actual != expected
                try:
                    if actual != expected:
                        return True  # KILLED: found inequality
                    else:
                        return False  # SURVIVED: equality holds
                except (TypeError, ValueError):
                    return None

        if isinstance(truth, Modal):
            # For Modal, we need to check if the invariant is violated
            state_val = evidence.bindings.get(truth.state_var)
            if state_val is not None:
                # Substitute the state value into the invariant
                invariant = truth.invariant
                state_sym = sym(truth.state_var)
                substituted = invariant.subs(state_sym, state_val)
                simplified = sp.simplify(substituted)

                if simplified is sp.false or simplified == False:  # noqa: E712
                    return True  # KILLED: invariant violated
                if simplified is sp.true or simplified == True:  # noqa: E712
                    return False  # SURVIVED: invariant holds

                # Try to evaluate numerically
                try:
                    if bool(simplified):
                        return False  # Invariant holds
                    else:
                        return True  # Invariant violated
                except (TypeError, ValueError):
                    return None

        return None

    def verify(self, truth: Truth, evidence: Evidence) -> VerdictResult:
        """Perform complete verification of a truth against evidence.

        This is the main entry point for verification. It:
        1. Constructs the falsification form
        2. Substitutes evidence
        3. Evaluates the result
        4. Returns a complete VerdictResult

        Args:
            truth: The truth to verify
            evidence: Evidence to test against

        Returns:
            VerdictResult with verdict, trace, and reasoning
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

        # Step 2: Substitute evidence
        result.add_trace(f"Evidence bindings: {evidence.bindings}")
        result.evidence = evidence

        # Check if we have all required bindings
        missing = set()
        for symbol in form.free_symbols:
            if symbol.name not in evidence.bindings:
                missing.add(symbol.name)

        if missing:
            result.reasoning = f"Missing evidence for: {missing}"
            result.add_trace(f"Cannot evaluate: missing {missing}")
            return result

        # Step 3: Try direct evaluation first (bypasses quantifier issues)
        direct_result = self._evaluate_falsification_directly(truth, evidence)
        if direct_result is not None:
            result.add_trace(f"Direct evaluation result: {direct_result}")
            if direct_result is True:
                result.verdict = Verdict.KILLED
                result.reasoning = f"Falsification condition met: {form.description}"
            else:
                result.verdict = Verdict.SURVIVED
                result.reasoning = "Falsification condition not met with given evidence"
            return result

        # Step 4: Fall back to symbolic evaluation
        substituted = self.substitute(form, evidence)
        result.add_trace(f"Substituted formula: {substituted}")

        eval_result = self.evaluate(substituted)
        result.add_trace(f"Evaluation result: {eval_result}")

        # Step 5: Determine verdict
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

    def verify_with_predicate(
        self, truth: Truth, value: Any, predicate_name: str = "check"
    ) -> VerdictResult:
        """Verify a truth using its built-in predicate method.

        For Empirical and Probabilistic truths that have check methods,
        this provides a simpler verification path.

        Args:
            truth: Truth with a check method
            value: Value to check
            predicate_name: Name of the predicate method

        Returns:
            VerdictResult based on predicate evaluation
        """
        result = VerdictResult(
            verdict=Verdict.UNCERTAIN,
            evidence=Evidence(bindings={"value": value}),
            trace=[f"Checking {truth.statement} with value: {value}"],
        )

        # Get the predicate method
        predicate = getattr(truth, predicate_name, None)
        if predicate is None:
            result.reasoning = f"Truth has no '{predicate_name}' method"
            return result

        # Evaluate predicate
        try:
            form = truth.falsify()
            result.form = form

            check_result = predicate(value)
            result.add_trace(f"Predicate result: {check_result}")

            if check_result:
                result.verdict = Verdict.SURVIVED
                result.reasoning = f"Value {value} satisfies predicate"
            else:
                result.verdict = Verdict.KILLED
                result.reasoning = f"Value {value} violates predicate: {form.description}"
        except Exception as e:
            result.verdict = Verdict.UNCERTAIN
            result.reasoning = f"Predicate evaluation failed: {e}"

        return result


# Convenience functions


def verify(truth: Truth, evidence: Evidence) -> VerdictResult:
    """Verify a truth against evidence.

    Convenience function that creates a Verifier and calls verify.

    Args:
        truth: The truth to verify
        evidence: Evidence to test against

    Returns:
        VerdictResult with verdict and reasoning
    """
    return Verifier().verify(truth, evidence)


def quick_check(truth: Truth, **bindings: Any) -> Verdict:
    """Quick check of a truth with bindings.

    Convenience function for simple cases.

    Args:
        truth: The truth to verify
        **bindings: Variable bindings as keyword arguments

    Returns:
        Just the Verdict (KILLED, SURVIVED, or UNCERTAIN)
    """
    evidence = Evidence(bindings=bindings)
    result = verify(truth, evidence)
    return result.verdict
