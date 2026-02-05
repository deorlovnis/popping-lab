"""Tests for veritas.symbolic module."""

from __future__ import annotations

import sympy as sp

from veritas import (
    and_,
    eq,
    exists,
    forall,
    implies,
    ne,
    negate,
    or_,
    simplify_verdict,
    sym,
)


class TestSym:
    """Tests for sym() function."""

    def test_creates_symbol(self) -> None:
        """sym() creates a SymPy Symbol."""
        x = sym("x")
        assert isinstance(x, sp.Symbol)
        assert x.name == "x"

    def test_caching(self) -> None:
        """sym() returns the same object for the same name."""
        x1 = sym("x")
        x2 = sym("x")
        assert x1 is x2

    def test_different_names(self) -> None:
        """sym() returns different objects for different names."""
        x = sym("x")
        y = sym("y")
        assert x is not y


class TestEq:
    """Tests for eq() function."""

    def test_creates_equality(self) -> None:
        """eq() creates a SymPy Equality."""
        x = sym("x")
        result = eq(x, 4)
        assert isinstance(result, sp.Equality)

    def test_with_numbers(self) -> None:
        """eq() works with plain numbers."""
        result = eq(2, 2)
        assert result == sp.Eq(2, 2)

    def test_with_symbols(self) -> None:
        """eq() works with symbols."""
        x = sym("x")
        y = sym("y")
        result = eq(x, y)
        assert isinstance(result, sp.Equality)


class TestNe:
    """Tests for ne() function."""

    def test_creates_inequality(self) -> None:
        """ne() creates a SymPy Ne."""
        x = sym("x")
        result = ne(x, 4)
        assert isinstance(result, sp.Ne)

    def test_with_numbers(self) -> None:
        """ne() works with plain numbers and evaluates to boolean."""
        result = ne(2, 3)
        # SymPy may simplify 2 != 3 to True directly
        assert result is sp.true or isinstance(result, sp.Ne)


class TestQuantifiers:
    """Tests for forall() and exists() functions."""

    def test_forall_single_var(self) -> None:
        """forall() creates quantified formula."""
        x = sym("x")
        pred = x > 0
        result = forall(x, pred)
        # Result should be a function application
        assert result is not None

    def test_exists_single_var(self) -> None:
        """exists() creates quantified formula."""
        x = sym("x")
        pred = ne(x, 0)
        result = exists(x, pred)
        assert result is not None

    def test_forall_multiple_vars(self) -> None:
        """forall() works with multiple variables."""
        x = sym("x")
        y = sym("y")
        pred = x + y > 0
        result = forall([x, y], pred)
        assert result is not None


class TestSimplifyVerdict:
    """Tests for simplify_verdict() function."""

    def test_true_equality(self) -> None:
        """simplify_verdict() returns True for true equality."""
        result = simplify_verdict(eq(4, 4))
        assert result is True

    def test_false_equality(self) -> None:
        """simplify_verdict() returns False for false equality."""
        result = simplify_verdict(eq(4, 5))
        assert result is False

    def test_true_inequality(self) -> None:
        """simplify_verdict() returns True for true inequality."""
        result = simplify_verdict(ne(4, 5))
        assert result is True

    def test_false_inequality(self) -> None:
        """simplify_verdict() returns False for false inequality."""
        result = simplify_verdict(ne(4, 4))
        assert result is False

    def test_symbolic_returns_none(self) -> None:
        """simplify_verdict() returns None for symbolic expressions."""
        x = sym("x")
        result = simplify_verdict(eq(x, 4))
        assert result is None


class TestLogicalConnectives:
    """Tests for implies(), negate(), and_(), or_()."""

    def test_implies(self) -> None:
        """implies() creates implication."""
        x = sym("x")
        result = implies(x > 0, x**2 > 0)
        assert isinstance(result, sp.Implies)

    def test_negate(self) -> None:
        """negate() creates negation."""
        x = sym("x")
        result = negate(x > 0)
        # SymPy may simplify ~(x > 0) to x <= 0
        assert isinstance(result, (sp.Not, sp.Rel))

    def test_and(self) -> None:
        """and_() creates conjunction."""
        x = sym("x")
        result = and_(x > 0, x < 10)
        assert isinstance(result, sp.And)

    def test_or(self) -> None:
        """or_() creates disjunction."""
        x = sym("x")
        result = or_(x < 0, x > 10)
        assert isinstance(result, sp.Or)
