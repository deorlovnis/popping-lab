"""Tests for veritas.engine module - Verifier and verification functions."""

from __future__ import annotations

import sympy as sp

from veritas import (
    Analytic,
    Evidence,
    Verdict,
    Verifier,
    quick_check,
    verify,
)


class TestVerifier:
    """Tests for Verifier class."""

    def test_creation(self) -> None:
        """Verifier can be created."""
        v = Verifier()
        assert v.strict is False

    def test_creation_strict(self) -> None:
        """Verifier can be created in strict mode."""
        v = Verifier(strict=True)
        assert v.strict is True

    def test_substitute(self) -> None:
        """substitute() replaces symbols with evidence values."""
        truth = Analytic(statement="test", lhs="x", rhs=4)
        form = truth.falsify()
        evidence = Evidence(bindings={"x": 5})
        v = Verifier()
        result = v.substitute(form, evidence)
        # The formula should have x substituted with 5
        assert result is not None

    def test_evaluate_true(self) -> None:
        """evaluate() returns True for true expression."""
        v = Verifier()
        # 5 != 4 is True
        expr = sp.Ne(5, 4)
        result = v.evaluate(expr)
        assert result is True

    def test_evaluate_false(self) -> None:
        """evaluate() returns False for false expression."""
        v = Verifier()
        # 4 != 4 is False
        expr = sp.Ne(4, 4)
        result = v.evaluate(expr)
        assert result is False

    def test_evaluate_symbolic_returns_none(self) -> None:
        """evaluate() returns None for symbolic expression."""
        v = Verifier()
        x = sp.Symbol("x")
        expr = sp.Ne(x, 4)
        result = v.evaluate(expr)
        assert result is None


class TestVerifierVerify:
    """Tests for Verifier.verify() method."""

    def test_verify_survived(self) -> None:
        """verify() returns SURVIVED when claim holds."""
        truth = Analytic(statement="2+2=4", lhs="result", rhs=4)
        evidence = Evidence(bindings={"result": 4, "x": 4})
        v = Verifier()
        result = v.verify(truth, evidence)
        assert result.verdict == Verdict.SURVIVED

    def test_verify_killed(self) -> None:
        """verify() returns KILLED when falsification condition met."""
        truth = Analytic(statement="2+2=4", lhs="result", rhs=4)
        # result=5 means result≠4 is True → falsification condition met → KILLED
        evidence = Evidence(bindings={"result": 5, "x": 5})
        v = Verifier()
        result = v.verify(truth, evidence)
        assert result.verdict == Verdict.KILLED

    def test_verify_uncertain_missing_evidence(self) -> None:
        """verify() returns UNCERTAIN when evidence is missing."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        evidence = Evidence(bindings={})  # Missing result binding
        v = Verifier()
        result = v.verify(truth, evidence)
        assert result.verdict == Verdict.UNCERTAIN
        assert "Missing" in result.reasoning

    def test_verify_populates_trace(self) -> None:
        """verify() populates the trace."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        evidence = Evidence(bindings={"result": 4, "x": 4})
        v = Verifier()
        result = v.verify(truth, evidence)
        assert len(result.trace) > 0

    def test_verify_sets_form_and_evidence(self) -> None:
        """verify() sets form and evidence on result."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        evidence = Evidence(bindings={"result": 4, "x": 4})
        v = Verifier()
        result = v.verify(truth, evidence)
        assert result.form is not None
        assert result.evidence is evidence


class TestConvenienceFunctions:
    """Tests for verify() and quick_check() functions."""

    def test_verify_function(self) -> None:
        """verify() function creates Verifier and verifies."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        evidence = Evidence(bindings={"result": 4, "x": 4})
        result = verify(truth, evidence)
        assert result.verdict == Verdict.SURVIVED

    def test_quick_check_survived(self) -> None:
        """quick_check() returns Verdict directly."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        verdict = quick_check(truth, result=4, x=4)
        assert verdict == Verdict.SURVIVED

    def test_quick_check_killed(self) -> None:
        """quick_check() returns KILLED for failing check."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        verdict = quick_check(truth, result=5, x=5)
        assert verdict == Verdict.KILLED
