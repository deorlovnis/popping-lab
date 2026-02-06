"""Tests for veritas.evidence module - Evidence, Verdict, VerdictResult."""

from __future__ import annotations

import sympy as sp

from veritas import Evidence, Verdict, VerdictResult
from veritas.truth import FalsificationForm


class TestVerdict:
    """Tests for Verdict enum."""

    def test_values(self) -> None:
        """Verdict has expected members."""
        assert Verdict.KILLED.value == "KILLED"
        assert Verdict.SURVIVED.value == "SURVIVED"
        assert Verdict.UNCERTAIN.value == "UNCERTAIN"


class TestEvidence:
    """Tests for Evidence dataclass."""

    def test_creation_with_bindings(self) -> None:
        """Evidence can be created with bindings."""
        e = Evidence(bindings={"x": 5, "y": 10})
        assert e.bindings == {"x": 5, "y": 10}

    def test_creation_with_source(self) -> None:
        """Evidence can have a source description."""
        e = Evidence(bindings={"x": 5}, source="test run")
        assert e.source == "test run"

    def test_creation_with_metadata(self) -> None:
        """Evidence can have metadata."""
        e = Evidence(bindings={"x": 5}, metadata={"timestamp": 123})
        assert e.metadata == {"timestamp": 123}

    def test_to_sympy(self) -> None:
        """to_sympy() converts bindings to SymPy symbols."""
        e = Evidence(bindings={"x": 5, "y": 10})
        sympy_bindings = e.to_sympy()
        assert sympy_bindings[sp.Symbol("x")] == 5
        assert sympy_bindings[sp.Symbol("y")] == 10


class TestVerdictResult:
    """Tests for VerdictResult dataclass."""

    def test_creation_minimal(self) -> None:
        """VerdictResult can be created with just verdict."""
        r = VerdictResult(verdict=Verdict.SURVIVED)
        assert r.verdict == Verdict.SURVIVED

    def test_creation_full(self) -> None:
        """VerdictResult can be created with all fields."""
        form = FalsificationForm(
            formula=sp.Symbol("x") > 0,
            free_symbols=frozenset({sp.Symbol("x")}),
        )
        evidence = Evidence(bindings={"x": 5})
        r = VerdictResult(
            verdict=Verdict.KILLED,
            form=form,
            evidence=evidence,
            trace=["step 1", "step 2"],
            reasoning="Found violation",
        )
        assert r.verdict == Verdict.KILLED
        assert r.form is form
        assert r.evidence is evidence
        assert r.trace == ["step 1", "step 2"]
        assert r.reasoning == "Found violation"

    def test_add_trace(self) -> None:
        """add_trace() appends to trace list."""
        r = VerdictResult(verdict=Verdict.SURVIVED)
        r.add_trace("Step 1")
        r.add_trace("Step 2")
        assert r.trace == ["Step 1", "Step 2"]
