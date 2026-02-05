"""Tests for veritas.evidence module - Evidence, Verdict, VerdictResult."""

from __future__ import annotations

import sympy as sp

from veritas import Evidence, Verdict, VerdictResult, sym
from veritas.truth import FalsificationForm


class TestVerdict:
    """Tests for Verdict enum."""

    def test_killed_value(self) -> None:
        """KILLED has expected string value."""
        assert str(Verdict.KILLED) == "KILLED"

    def test_survived_value(self) -> None:
        """SURVIVED has expected string value."""
        assert str(Verdict.SURVIVED) == "SURVIVED"

    def test_uncertain_value(self) -> None:
        """UNCERTAIN has expected string value."""
        assert str(Verdict.UNCERTAIN) == "UNCERTAIN"


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
        assert sympy_bindings[sym("x")] == 5
        assert sympy_bindings[sym("y")] == 10

    def test_get_existing(self) -> None:
        """get() returns binding value."""
        e = Evidence(bindings={"x": 5})
        assert e.get("x") == 5

    def test_get_missing_default(self) -> None:
        """get() returns default for missing binding."""
        e = Evidence(bindings={"x": 5})
        assert e.get("y") is None
        assert e.get("y", 0) == 0

    def test_contains(self) -> None:
        """__contains__ checks binding presence."""
        e = Evidence(bindings={"x": 5})
        assert "x" in e
        assert "y" not in e


class TestVerdictResult:
    """Tests for VerdictResult dataclass."""

    def test_creation_minimal(self) -> None:
        """VerdictResult can be created with just verdict."""
        r = VerdictResult(verdict=Verdict.SURVIVED)
        assert r.verdict == Verdict.SURVIVED

    def test_creation_full(self) -> None:
        """VerdictResult can be created with all fields."""
        form = FalsificationForm(
            formula=sym("x") > 0,
            free_symbols=frozenset({sym("x")}),
        )
        evidence = Evidence(bindings={"x": 5})
        r = VerdictResult(
            verdict=Verdict.KILLED,
            form=form,
            evidence=evidence,
            trace=["step 1", "step 2"],
            reasoning="Found violation",
            mutations=["New claim"],
        )
        assert r.verdict == Verdict.KILLED
        assert r.form is form
        assert r.evidence is evidence
        assert r.trace == ["step 1", "step 2"]
        assert r.reasoning == "Found violation"
        assert r.mutations == ["New claim"]

    def test_is_killed(self) -> None:
        """is_killed() returns True for KILLED verdict."""
        r = VerdictResult(verdict=Verdict.KILLED)
        assert r.is_killed() is True
        assert r.is_survived() is False
        assert r.is_uncertain() is False

    def test_is_survived(self) -> None:
        """is_survived() returns True for SURVIVED verdict."""
        r = VerdictResult(verdict=Verdict.SURVIVED)
        assert r.is_killed() is False
        assert r.is_survived() is True
        assert r.is_uncertain() is False

    def test_is_uncertain(self) -> None:
        """is_uncertain() returns True for UNCERTAIN verdict."""
        r = VerdictResult(verdict=Verdict.UNCERTAIN)
        assert r.is_killed() is False
        assert r.is_survived() is False
        assert r.is_uncertain() is True

    def test_add_trace(self) -> None:
        """add_trace() appends to trace list."""
        r = VerdictResult(verdict=Verdict.SURVIVED)
        r.add_trace("Step 1")
        r.add_trace("Step 2")
        assert r.trace == ["Step 1", "Step 2"]

    def test_add_mutation(self) -> None:
        """add_mutation() appends to mutations list."""
        r = VerdictResult(verdict=Verdict.SURVIVED)
        r.add_mutation("New claim 1")
        r.add_mutation("New claim 2")
        assert r.mutations == ["New claim 1", "New claim 2"]

    def test_to_dict(self) -> None:
        """to_dict() returns serializable dictionary."""
        r = VerdictResult(
            verdict=Verdict.SURVIVED,
            reasoning="Test passed",
            trace=["step 1"],
            mutations=["mutation 1"],
        )
        d = r.to_dict()
        assert d["verdict"] == "SURVIVED"
        assert d["reasoning"] == "Test passed"
        assert d["trace"] == ["step 1"]
        assert d["mutations"] == ["mutation 1"]

    def test_str(self) -> None:
        """__str__ returns human-readable string."""
        r = VerdictResult(
            verdict=Verdict.SURVIVED,
            reasoning="Claim held up",
        )
        s = str(r)
        assert "SURVIVED" in s
        assert "Claim held up" in s
