"""Symbolic formula building blocks for Veritas.

This module provides the foundation for symbolic reasoning:
- Symbol creation with caching
- Formula builders (equality, inequality)
- Quantifiers (forall, exists)
- Verdict simplification
"""

from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

import sympy as sp
from sympy.logic.boolalg import Boolean

if TYPE_CHECKING:
    from collections.abc import Sequence


@lru_cache(maxsize=256)
def sym(name: str) -> sp.Symbol:
    """Create or retrieve a cached symbol.

    Args:
        name: Symbol name (e.g., 'x', 'y', 'result')

    Returns:
        A SymPy Symbol, cached for reuse.

    Example:
        >>> x = sym('x')
        >>> x is sym('x')  # Same object
        True
    """
    return sp.Symbol(name)


def eq(a: sp.Basic | int | float, b: sp.Basic | int | float) -> sp.Equality:
    """Create an equality formula: a = b.

    Args:
        a: Left side of equality
        b: Right side of equality

    Returns:
        SymPy Equality object

    Example:
        >>> eq(sym('x'), 4)
        Eq(x, 4)
    """
    return sp.Eq(a, b)


def ne(a: sp.Basic | int | float, b: sp.Basic | int | float) -> sp.Ne:
    """Create an inequality formula: a ≠ b.

    Args:
        a: Left side
        b: Right side

    Returns:
        SymPy inequality (Ne) object

    Example:
        >>> ne(sym('x'), 4)
        Ne(x, 4)
    """
    return sp.Ne(a, b)


def forall(var: sp.Symbol | Sequence[sp.Symbol], pred: Boolean) -> sp.Basic:
    """Universal quantifier: ∀var. pred.

    Note: SymPy doesn't have native first-order quantifiers.
    This creates a symbolic representation for documentation
    and uses SymPy's ForAll when available in logic module.

    Args:
        var: Variable(s) to quantify over
        pred: Predicate that must hold for all values

    Returns:
        Symbolic representation of universal quantification

    Example:
        >>> x = sym('x')
        >>> forall(x, x >= 0)  # ∀x. x ≥ 0
    """
    # SymPy's logic module has limited quantifier support
    # We use a Function to represent quantification symbolically
    if isinstance(var, sp.Symbol):
        vars_tuple = (var,)
    else:
        vars_tuple = tuple(var)

    # Create a symbolic function representing ForAll
    forall_func = sp.Function("ForAll")
    return forall_func(*vars_tuple, pred)


def exists(var: sp.Symbol | Sequence[sp.Symbol], pred: Boolean) -> sp.Basic:
    """Existential quantifier: ∃var. pred.

    Creates a symbolic representation of existential quantification.
    The key use case is falsification: ∃x. f(x) ≠ expected

    Args:
        var: Variable(s) to quantify over
        pred: Predicate that must hold for some value

    Returns:
        Symbolic representation of existential quantification

    Example:
        >>> x = sym('x')
        >>> exists(x, ne(x**2, 4))  # ∃x. x² ≠ 4
    """
    if isinstance(var, sp.Symbol):
        vars_tuple = (var,)
    else:
        vars_tuple = tuple(var)

    exists_func = sp.Function("Exists")
    return exists_func(*vars_tuple, pred)


def simplify_verdict(expr: sp.Basic) -> bool | None:
    """Attempt to simplify an expression to a boolean verdict.

    Args:
        expr: SymPy expression to evaluate

    Returns:
        True if expression simplifies to True
        False if expression simplifies to False
        None if expression cannot be determined

    Example:
        >>> simplify_verdict(eq(4, 4))
        True
        >>> simplify_verdict(eq(sym('x'), 4))  # Can't determine
        None
    """
    simplified = sp.simplify(expr)

    # Check for boolean truth values
    if simplified is sp.true or simplified == True:  # noqa: E712
        return True
    if simplified is sp.false or simplified == False:  # noqa: E712
        return False

    # For Equality/Inequality, try to evaluate
    if isinstance(simplified, sp.Equality):
        # If both sides are concrete, we can evaluate
        if simplified.lhs.is_number and simplified.rhs.is_number:
            return bool(simplified.lhs == simplified.rhs)

    if isinstance(simplified, sp.Ne):
        if simplified.lhs.is_number and simplified.rhs.is_number:
            return bool(simplified.lhs != simplified.rhs)

    # Cannot determine
    return None


def implies(p: Boolean, q: Boolean) -> sp.Implies:
    """Create an implication formula: p → q.

    Args:
        p: Antecedent
        q: Consequent

    Returns:
        SymPy Implies object

    Example:
        >>> x = sym('x')
        >>> implies(x > 0, x**2 > 0)  # x > 0 → x² > 0
    """
    return sp.Implies(p, q)


def negate(expr: Boolean) -> sp.Not:
    """Negate a boolean expression: ¬expr.

    Args:
        expr: Expression to negate

    Returns:
        SymPy Not object

    Example:
        >>> negate(sym('x') > 0)  # ¬(x > 0)
    """
    return sp.Not(expr)


def and_(*exprs: Boolean) -> Boolean:
    """Logical conjunction: expr₁ ∧ expr₂ ∧ ...

    Args:
        exprs: Boolean expressions to combine

    Returns:
        SymPy And object

    Example:
        >>> x = sym('x')
        >>> and_(x > 0, x < 10)  # 0 < x < 10
    """
    return sp.And(*exprs)


def or_(*exprs: Boolean) -> Boolean:
    """Logical disjunction: expr₁ ∨ expr₂ ∨ ...

    Args:
        exprs: Boolean expressions to combine

    Returns:
        SymPy Or object

    Example:
        >>> x = sym('x')
        >>> or_(x < 0, x > 10)  # x < 0 ∨ x > 10
    """
    return sp.Or(*exprs)
