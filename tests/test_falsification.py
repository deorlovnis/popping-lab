"""Tests for veritas.falsification module."""

from __future__ import annotations

import sympy as sp

from veritas import (
    Analytic,
    Evidence,
    Verdict,
    falsify,
    quick_check,
)
from veritas.falsification import _evaluate, _substitute


class TestSubstitute:
    """Tests for _substitute()."""

    def test_replaces_symbols(self) -> None:
        """_substitute() replaces symbols with evidence values."""
        truth = Analytic(statement="test", lhs="x", rhs=4)
        form = truth.falsify()
        evidence = Evidence(bindings={"x": 5})
        result = _substitute(form, evidence)
        assert result is not None


class TestEvaluate:
    """Tests for _evaluate()."""

    def test_true(self) -> None:
        """_evaluate() returns True for true expression."""
        expr = sp.Ne(5, 4)
        assert _evaluate(expr) is True

    def test_false(self) -> None:
        """_evaluate() returns False for false expression."""
        expr = sp.Ne(4, 4)
        assert _evaluate(expr) is False

    def test_symbolic_returns_none(self) -> None:
        """_evaluate() returns None for symbolic expression."""
        x = sp.Symbol("x")
        expr = sp.Ne(x, 4)
        assert _evaluate(expr) is None


class TestFalsify:
    """Tests for falsify()."""

    def test_survived(self) -> None:
        """falsify() returns SURVIVED when claim holds."""
        truth = Analytic(statement="2+2=4", lhs="result", rhs=4)
        evidence = Evidence(bindings={"result": 4, "x": 4})
        result = falsify(truth, evidence)
        assert result.verdict == Verdict.SURVIVED

    def test_killed(self) -> None:
        """falsify() returns KILLED when falsification condition met."""
        truth = Analytic(statement="2+2=4", lhs="result", rhs=4)
        evidence = Evidence(bindings={"result": 5, "x": 5})
        result = falsify(truth, evidence)
        assert result.verdict == Verdict.KILLED

    def test_uncertain_missing_evidence(self) -> None:
        """falsify() returns UNCERTAIN when evidence is missing."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        evidence = Evidence(bindings={})
        result = falsify(truth, evidence)
        assert result.verdict == Verdict.UNCERTAIN
        assert "Missing" in result.reasoning

    def test_populates_trace(self) -> None:
        """falsify() populates the trace."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        evidence = Evidence(bindings={"result": 4, "x": 4})
        result = falsify(truth, evidence)
        assert len(result.trace) > 0

    def test_sets_form_and_evidence(self) -> None:
        """falsify() sets form and evidence on result."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        evidence = Evidence(bindings={"result": 4, "x": 4})
        result = falsify(truth, evidence)
        assert result.form is not None
        assert result.evidence is evidence


class TestQuickCheck:
    """Tests for quick_check()."""

    def test_survived(self) -> None:
        """quick_check() returns Verdict directly."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        verdict = quick_check(truth, result=4, x=4)
        assert verdict == Verdict.SURVIVED

    def test_killed(self) -> None:
        """quick_check() returns KILLED for failing check."""
        truth = Analytic(statement="test", lhs="result", rhs=4)
        verdict = quick_check(truth, result=5, x=5)
        assert verdict == Verdict.KILLED
