"""Core truth types for Veritas falsification.

This module defines the Truth protocol and four concrete implementations:
- Analytic: equality claims (∃x: f(x) ≠ y)
- Modal: necessity claims (◇¬P, invariant violation)
- Empirical: observation-based claims
- Probabilistic: threshold-based claims (P(X) ≤ t)

Each truth type knows how to construct its own falsification form.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

import sympy as sp

if TYPE_CHECKING:
    from collections.abc import Callable


@runtime_checkable
class Truth(Protocol):
    """Protocol for any truth that can be falsified.

    A Truth represents a claim about the world that can be tested.
    It must provide:
    - A human-readable statement
    - A method to construct its falsification form
    - A string representation for debugging
    """

    @property
    def statement(self) -> str:
        """Human-readable statement of the claim."""
        ...

    def falsify(self) -> FalsificationForm:
        """Construct the falsification form for this truth.

        Returns:
            A FalsificationForm that, if satisfied, kills the claim.
        """
        ...

    def __repr__(self) -> str:
        """String representation for debugging."""
        ...


@dataclass(frozen=True)
class FalsificationForm:
    """A formula that, if satisfied, falsifies a claim.

    The falsification form is the logical structure we're trying to satisfy
    to kill a claim. It contains:
    - The SymPy formula
    - Free symbols that need binding
    - A check function for concrete evaluation
    """

    formula: sp.Basic
    """The SymPy formula representing the falsification condition."""

    free_symbols: frozenset[sp.Symbol] = field(default_factory=frozenset)
    """Symbols in the formula that require binding to concrete values."""

    description: str = ""
    """Human-readable description of what satisfies this form."""

    def check(self, **bindings: Any) -> bool | None:
        """Check if the falsification condition is met with given bindings.

        Args:
            **bindings: Variable name to value mappings

        Returns:
            True if falsification condition is met (claim is KILLED)
            False if condition is not met
            None if cannot be determined
        """
        substituted = self.formula
        for name, value in bindings.items():
            symbol = sp.Symbol(name)
            substituted = substituted.subs(symbol, value)

        simplified = sp.simplify(substituted)

        if simplified is sp.true or simplified == True:  # noqa: E712
            return True
        if simplified is sp.false or simplified == False:  # noqa: E712
            return False
        return None


@dataclass(frozen=True)
class Analytic:
    """An analytic truth: equality claims that can be falsified by counterexample.

    Analytic truths are claims of the form "f(x) = y" that are falsified
    by finding an x where f(x) ≠ y.

    Maps to old claim types:
    - equality: ∃x: f(x) ≠ expected
    - membership: ∃x: x ∉ S (element fails predicate)
    - ordering: ∃x,y: order(x,y) violated

    Example:
        >>> t = Analytic(
        ...     statement="add(2, 2) equals 4",
        ...     lhs="result",
        ...     rhs=4
        ... )
        >>> form = t.falsify()  # ∃result: result ≠ 4
    """

    statement: str
    """Human-readable statement of the equality claim."""

    lhs: sp.Basic | str
    """Left-hand side: the computed/actual value (or symbol name)."""

    rhs: sp.Basic | int | float | None
    """Right-hand side: the expected value."""

    var_name: str = "x"
    """Name for the free variable in the falsification form."""

    def falsify(self) -> FalsificationForm:
        """Construct falsification: ∃x: lhs ≠ rhs.

        Returns:
            FalsificationForm where satisfaction means finding inequality.
        """
        lhs = sp.Symbol(self.lhs) if isinstance(self.lhs, str) else self.lhs

        # Falsification form: lhs ≠ rhs
        formula = sp.Ne(lhs, self.rhs)

        return FalsificationForm(
            formula=formula,
            free_symbols=frozenset(formula.free_symbols),
            description=f"Find {self.var_name} where {lhs} ≠ {self.rhs}",
        )

    def __repr__(self) -> str:
        return f"Analytic({self.statement!r})"


@dataclass(frozen=True)
class Modal:
    """A modal truth: necessity claims that can be falsified by possible violation.

    Modal truths are claims of the form "□P" (P necessarily holds) that are
    falsified by showing ◇¬P (it's possible that P doesn't hold).

    Maps to old claim type:
    - invariant: Find state where ¬P

    Example:
        >>> t = Modal(
        ...     statement="balance >= 0 after any transaction",
        ...     invariant=sym('balance') >= 0
        ... )
        >>> form = t.falsify()  # ◇(balance < 0)
    """

    statement: str
    """Human-readable statement of the invariant claim."""

    invariant: sp.Basic
    """The property P that must necessarily hold."""

    state_var: str = "state"
    """Name for the state variable in the falsification form."""

    def falsify(self) -> FalsificationForm:
        """Construct falsification: ◇¬P (possible violation).

        Returns:
            FalsificationForm where satisfaction means finding a violation.
        """
        # Falsification: ¬P (invariant violated)
        formula = sp.Not(self.invariant)

        return FalsificationForm(
            formula=formula,
            free_symbols=frozenset(formula.free_symbols),
            description=f"Find {self.state_var} where ¬({self.invariant})",
        )

    def __repr__(self) -> str:
        return f"Modal({self.statement!r})"


@dataclass(frozen=True)
class Empirical:
    """An empirical truth: observation-based claims.

    Empirical truths are claims grounded in observation. They are falsified
    when an observation contradicts the claim.

    Maps to old claim types:
    - grounding: Observation contradicts support
    - feasibility: Observation shows blocker

    Example:
        >>> t = Empirical(
        ...     statement="API endpoint exists and returns 200",
        ...     observation_var="status_code",
        ...     expected_predicate=lambda s: s == 200
        ... )
    """

    statement: str
    """Human-readable statement of the empirical claim."""

    observation_var: str = "observation"
    """Name for the observation variable."""

    expected_predicate: Callable[[Any], bool] | None = None
    """Predicate that observations should satisfy."""

    contradiction_description: str = ""
    """Description of what would contradict this claim."""

    def falsify(self) -> FalsificationForm:
        """Construct falsification: ∃obs: contradicts(obs).

        Returns:
            FalsificationForm where satisfaction means finding contradiction.
        """
        var = sp.Symbol(self.observation_var)

        # Create a symbolic contradiction predicate
        formula = sp.Function("Contradicts")(var)

        desc = self.contradiction_description or f"Find {self.observation_var} that contradicts claim"

        return FalsificationForm(
            formula=formula,
            free_symbols=frozenset(formula.free_symbols),
            description=desc,
        )

    def check_observation(self, value: Any) -> bool:
        """Check if an observation satisfies or contradicts the claim.

        Args:
            value: The observed value

        Returns:
            True if observation satisfies expected predicate
            False if observation contradicts (claim is KILLED)
        """
        if self.expected_predicate is None:
            return True  # No predicate means any observation is ok
        return self.expected_predicate(value)

    def __repr__(self) -> str:
        return f"Empirical({self.statement!r})"


@dataclass(frozen=True)
class Probabilistic:
    """A probabilistic truth: threshold-based claims.

    Probabilistic truths are claims about probabilities or rates that are
    falsified when the observed probability crosses a threshold.

    Example:
        >>> t = Probabilistic(
        ...     statement="Model accuracy > 60%",
        ...     metric="accuracy",
        ...     threshold=0.6,
        ...     direction=">"
        ... )
    """

    statement: str
    """Human-readable statement of the probabilistic claim."""

    metric: str = "value"
    """Name of the metric being measured."""

    threshold: float = 0.5
    """The threshold value."""

    direction: str = ">"
    """Comparison direction: '>', '>=', '<', '<=', '='."""

    def falsify(self) -> FalsificationForm:
        """Construct falsification: ∃metric: ¬(metric op threshold).

        Returns:
            FalsificationForm where satisfaction means threshold violation.
        """
        var = sp.Symbol(self.metric)

        # Construct the expected condition
        if self.direction == ">":
            expected = var > self.threshold
        elif self.direction == ">=":
            expected = var >= self.threshold
        elif self.direction == "<":
            expected = var < self.threshold
        elif self.direction == "<=":
            expected = var <= self.threshold
        else:  # "="
            expected = sp.Eq(var, self.threshold)

        # Falsification: ¬(metric op threshold)
        formula = sp.Not(expected)

        return FalsificationForm(
            formula=formula,
            free_symbols=frozenset(formula.free_symbols),
            description=f"Find {self.metric} where ¬({self.metric} {self.direction} {self.threshold})",
        )

    def check_threshold(self, value: float) -> bool:
        """Check if a value satisfies the threshold.

        Args:
            value: The measured value

        Returns:
            True if value satisfies threshold
            False if threshold is violated (claim is KILLED)
        """
        if self.direction == ">":
            return value > self.threshold
        elif self.direction == ">=":
            return value >= self.threshold
        elif self.direction == "<":
            return value < self.threshold
        elif self.direction == "<=":
            return value <= self.threshold
        else:  # "="
            return value == self.threshold

    def __repr__(self) -> str:
        return f"Probabilistic({self.statement!r})"
