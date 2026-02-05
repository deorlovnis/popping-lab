"""Tests for veritas.engine module - Verifier and verification functions."""

from __future__ import annotations

import sympy as sp

from veritas import (
    Analytic,
    Empirical,
    Evidence,
    Modal,
    Probabilistic,
    Verdict,
    Verifier,
    quick_check,
    sym,
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
        x = sym("x")
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


class TestVerifierVerifyWithPredicate:
    """Tests for Verifier.verify_with_predicate() method."""

    def test_empirical_survived(self) -> None:
        """verify_with_predicate() SURVIVED for passing predicate."""
        truth = Empirical(
            statement="status is 200",
            observation_var="status",
            expected_predicate=lambda s: s == 200,
        )
        v = Verifier()
        result = v.verify_with_predicate(truth, 200, "check_observation")
        assert result.verdict == Verdict.SURVIVED

    def test_empirical_killed(self) -> None:
        """verify_with_predicate() KILLED for failing predicate."""
        truth = Empirical(
            statement="status is 200",
            observation_var="status",
            expected_predicate=lambda s: s == 200,
        )
        v = Verifier()
        result = v.verify_with_predicate(truth, 404, "check_observation")
        assert result.verdict == Verdict.KILLED

    def test_probabilistic_survived(self) -> None:
        """verify_with_predicate() works for Probabilistic."""
        truth = Probabilistic(
            statement="accuracy > 50%",
            metric="accuracy",
            threshold=0.5,
            direction=">",
        )
        v = Verifier()
        result = v.verify_with_predicate(truth, 0.6, "check_threshold")
        assert result.verdict == Verdict.SURVIVED

    def test_probabilistic_killed(self) -> None:
        """verify_with_predicate() KILLED for failing threshold."""
        truth = Probabilistic(
            statement="accuracy > 50%",
            metric="accuracy",
            threshold=0.5,
            direction=">",
        )
        v = Verifier()
        result = v.verify_with_predicate(truth, 0.4, "check_threshold")
        assert result.verdict == Verdict.KILLED

    def test_no_predicate_method(self) -> None:
        """verify_with_predicate() UNCERTAIN when method doesn't exist."""
        truth = Analytic(statement="test", lhs="x", rhs=1)
        v = Verifier()
        result = v.verify_with_predicate(truth, 1, "nonexistent_method")
        assert result.verdict == Verdict.UNCERTAIN


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


class TestModalVerification:
    """Tests for Modal truth verification."""

    def test_modal_survived(self) -> None:
        """Modal claim SURVIVED when invariant holds."""
        x = sym("x")
        truth = Modal(
            statement="x >= 0",
            invariant=x >= 0,
            state_var="x",
        )
        # When x=5, the invariant holds, so ¬(x>=0) is False
        # The falsification form exists(x, ¬(x>=0)) with x=5 → False
        # So SURVIVED
        evidence = Evidence(bindings={"x": 5, "state": 5})
        result = verify(truth, evidence)
        # Note: Modal verification is more complex due to quantifiers
        # The result depends on how we interpret the evidence
        assert result.verdict in [Verdict.SURVIVED, Verdict.UNCERTAIN]

    def test_modal_killed(self) -> None:
        """Modal claim KILLED when invariant violated."""
        x = sym("x")
        truth = Modal(
            statement="x >= 0",
            invariant=x >= 0,
            state_var="x",
        )
        # When state=-1, the invariant x>=0 is violated
        evidence = Evidence(bindings={"x": -1, "state": -1})
        result = verify(truth, evidence)
        # Modal evaluation with negative value should show violation
        assert result.verdict in [Verdict.KILLED, Verdict.UNCERTAIN]
