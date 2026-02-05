"""Pytest configuration and shared fixtures for Veritas tests."""

from __future__ import annotations

import pytest
import sympy as sp

from veritas import (
    Analytic,
    Empirical,
    Evidence,
    Modal,
    Probabilistic,
    sym,
)


@pytest.fixture
def x() -> sp.Symbol:
    """A reusable symbol 'x'."""
    return sym("x")


@pytest.fixture
def y() -> sp.Symbol:
    """A reusable symbol 'y'."""
    return sym("y")


@pytest.fixture
def result() -> sp.Symbol:
    """A reusable symbol 'result'."""
    return sym("result")


@pytest.fixture
def simple_equality() -> Analytic:
    """A simple equality claim: 2+2=4."""
    return Analytic(
        statement="2+2 equals 4",
        lhs="result",
        rhs=4,
    )


@pytest.fixture
def simple_invariant(x: sp.Symbol) -> Modal:
    """A simple invariant: x >= 0."""
    return Modal(
        statement="x is non-negative",
        invariant=x >= 0,
        state_var="x",
    )


@pytest.fixture
def simple_empirical() -> Empirical:
    """A simple empirical claim: status is 200."""
    return Empirical(
        statement="API returns 200",
        observation_var="status",
        expected_predicate=lambda s: s == 200,
        contradiction_description="status != 200",
    )


@pytest.fixture
def simple_probabilistic() -> Probabilistic:
    """A simple probabilistic claim: accuracy > 0.5."""
    return Probabilistic(
        statement="Model accuracy > 50%",
        metric="accuracy",
        threshold=0.5,
        direction=">",
    )


@pytest.fixture
def empty_evidence() -> Evidence:
    """Empty evidence with no bindings."""
    return Evidence(bindings={})


@pytest.fixture
def evidence_with_result() -> Evidence:
    """Evidence with result=4."""
    return Evidence(bindings={"result": 4})


@pytest.fixture
def evidence_with_wrong_result() -> Evidence:
    """Evidence with result=5 (wrong)."""
    return Evidence(bindings={"result": 5})
