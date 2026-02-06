"""Tests for veritas.truth module - Truth types and FalsificationForm."""

from __future__ import annotations

import sympy as sp

from veritas import (
    Analytic,
    Empirical,
    FalsificationForm,
    Modal,
    Probabilistic,
    Truth,
)


class TestTruthProtocol:
    """Tests for Truth protocol compliance."""

    def test_analytic_is_truth(self) -> None:
        """Analytic implements Truth protocol."""
        t = Analytic(statement="test", lhs="x", rhs=1)
        assert isinstance(t, Truth)

    def test_modal_is_truth(self) -> None:
        """Modal implements Truth protocol."""
        t = Modal(statement="test", invariant=sp.Symbol("x") >= 0)
        assert isinstance(t, Truth)

    def test_empirical_is_truth(self) -> None:
        """Empirical implements Truth protocol."""
        t = Empirical(statement="test", observation_var="x")
        assert isinstance(t, Truth)

    def test_probabilistic_is_truth(self) -> None:
        """Probabilistic implements Truth protocol."""
        t = Probabilistic(statement="test", metric="x", threshold=0.5)
        assert isinstance(t, Truth)


class TestFalsificationForm:
    """Tests for FalsificationForm."""

    def test_check_with_true_binding(self) -> None:
        """check() returns True when falsification condition is met."""
        form = FalsificationForm(
            formula=sp.Ne(sp.Symbol("x"), 4),
            free_symbols=frozenset({sp.Symbol("x")}),
            description="Find x where x ≠ 4",
        )
        # x=5 means x≠4 is True (falsification condition met)
        result = form.check(x=5)
        assert result is True

    def test_check_with_false_binding(self) -> None:
        """check() returns False when falsification condition not met."""
        form = FalsificationForm(
            formula=sp.Ne(sp.Symbol("x"), 4),
            free_symbols=frozenset({sp.Symbol("x")}),
            description="Find x where x ≠ 4",
        )
        # x=4 means x≠4 is False (falsification condition not met)
        result = form.check(x=4)
        assert result is False


class TestAnalytic:
    """Tests for Analytic truth type."""

    def test_statement_property(self) -> None:
        """statement property returns the claim statement."""
        t = Analytic(statement="2+2=4", lhs="result", rhs=4)
        assert t.statement == "2+2=4"

    def test_falsify_creates_form(self) -> None:
        """falsify() creates a FalsificationForm."""
        t = Analytic(statement="2+2=4", lhs="result", rhs=4)
        form = t.falsify()
        assert isinstance(form, FalsificationForm)
        assert form.description == "Find x where result ≠ 4"

    def test_falsify_form_check_survives(self) -> None:
        """Falsification check returns False when claim is true."""
        t = Analytic(statement="2+2=4", lhs="result", rhs=4)
        form = t.falsify()
        # If result=4, then result≠4 is False (claim survives)
        result = form.check(result=4)
        assert result is False

    def test_repr(self) -> None:
        """__repr__ returns useful string."""
        t = Analytic(statement="test", lhs="x", rhs=1)
        assert "Analytic" in repr(t)
        assert "test" in repr(t)


class TestModal:
    """Tests for Modal truth type."""

    def test_statement_property(self) -> None:
        """statement property returns the claim statement."""
        t = Modal(statement="x >= 0 always", invariant=sp.Symbol("x") >= 0)
        assert t.statement == "x >= 0 always"

    def test_falsify_creates_form(self) -> None:
        """falsify() creates a FalsificationForm for invariant violation."""
        x = sp.Symbol("x")
        t = Modal(statement="x >= 0", invariant=x >= 0)
        form = t.falsify()
        assert isinstance(form, FalsificationForm)
        # Should seek ¬(x >= 0), i.e., x < 0
        assert sp.Symbol("x") in form.free_symbols

    def test_repr(self) -> None:
        """__repr__ returns useful string."""
        t = Modal(statement="test", invariant=sp.Symbol("x") >= 0)
        assert "Modal" in repr(t)


class TestEmpirical:
    """Tests for Empirical truth type."""

    def test_statement_property(self) -> None:
        """statement property returns the claim statement."""
        t = Empirical(statement="API works", observation_var="status")
        assert t.statement == "API works"

    def test_falsify_creates_form(self) -> None:
        """falsify() creates a FalsificationForm."""
        t = Empirical(statement="API works", observation_var="status")
        form = t.falsify()
        assert isinstance(form, FalsificationForm)

    def test_check_observation_with_predicate(self) -> None:
        """check_observation() uses the predicate."""
        t = Empirical(
            statement="status is 200",
            observation_var="status",
            expected_predicate=lambda s: s == 200,
        )
        assert t.check_observation(200) is True
        assert t.check_observation(404) is False

    def test_check_observation_without_predicate(self) -> None:
        """check_observation() returns True with no predicate."""
        t = Empirical(statement="test", observation_var="x")
        assert t.check_observation("anything") is True

    def test_repr(self) -> None:
        """__repr__ returns useful string."""
        t = Empirical(statement="test", observation_var="x")
        assert "Empirical" in repr(t)


class TestProbabilistic:
    """Tests for Probabilistic truth type."""

    def test_statement_property(self) -> None:
        """statement property returns the claim statement."""
        t = Probabilistic(statement="accuracy > 50%", metric="acc", threshold=0.5)
        assert t.statement == "accuracy > 50%"

    def test_falsify_creates_form(self) -> None:
        """falsify() creates a FalsificationForm."""
        t = Probabilistic(statement="test", metric="acc", threshold=0.5)
        form = t.falsify()
        assert isinstance(form, FalsificationForm)

    def test_check_threshold_greater_than(self) -> None:
        """check_threshold() works for > comparison."""
        t = Probabilistic(statement="test", metric="acc", threshold=0.5, direction=">")
        assert t.check_threshold(0.6) is True
        assert t.check_threshold(0.5) is False
        assert t.check_threshold(0.4) is False

    def test_check_threshold_greater_equal(self) -> None:
        """check_threshold() works for >= comparison."""
        t = Probabilistic(statement="test", metric="acc", threshold=0.5, direction=">=")
        assert t.check_threshold(0.6) is True
        assert t.check_threshold(0.5) is True
        assert t.check_threshold(0.4) is False

    def test_check_threshold_less_than(self) -> None:
        """check_threshold() works for < comparison."""
        t = Probabilistic(statement="test", metric="acc", threshold=0.5, direction="<")
        assert t.check_threshold(0.4) is True
        assert t.check_threshold(0.5) is False

    def test_check_threshold_less_equal(self) -> None:
        """check_threshold() works for <= comparison."""
        t = Probabilistic(statement="test", metric="acc", threshold=0.5, direction="<=")
        assert t.check_threshold(0.4) is True
        assert t.check_threshold(0.5) is True
        assert t.check_threshold(0.6) is False

    def test_check_threshold_equal(self) -> None:
        """check_threshold() works for = comparison."""
        t = Probabilistic(statement="test", metric="acc", threshold=0.5, direction="=")
        assert t.check_threshold(0.5) is True
        assert t.check_threshold(0.6) is False

    def test_repr(self) -> None:
        """__repr__ returns useful string."""
        t = Probabilistic(statement="test", metric="acc", threshold=0.5)
        assert "Probabilistic" in repr(t)
