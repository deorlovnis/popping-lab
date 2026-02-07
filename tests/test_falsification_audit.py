"""Falsification audit: trace one claim through the entire pipeline.

This test exists to verify that falsification.py and evidence.py actually work
in the simplest possible case. It walks through each step explicitly
so a human can read the output and see what happens.

Claim: 2 + 2 = 4
"""

from __future__ import annotations

import sympy as sp

from veritas import Analytic, Evidence, Verdict, falsify
from veritas.falsification import _evaluate, _substitute


def test_falsification_audit_claim_survives():
    """The simplest possible claim: 2+2=4, evidence says result is 4."""

    # --- Step 1: Define the claim ---
    truth = Analytic(statement="2 + 2 equals 4", lhs="result", rhs=4)

    # The falsification form asks: "can we find result ≠ 4?"
    form = truth.falsify()
    assert form.formula == sp.Ne(sp.Symbol("result"), 4)
    assert form.free_symbols == frozenset({sp.Symbol("result")})

    # --- Step 2: Provide evidence ---
    evidence = Evidence(bindings={"result": 4})

    # Evidence converts to sympy: {Symbol('result'): 4}
    sympy_bindings = evidence.to_sympy()
    assert sympy_bindings == {sp.Symbol("result"): 4}

    # --- Step 3: Substitute evidence into the formula ---
    substituted = _substitute(form, evidence)

    # After substitution: Ne(4, 4) — "is 4 ≠ 4?"
    assert substituted == sp.Ne(4, 4)

    # --- Step 4: Evaluate ---
    eval_result = _evaluate(substituted)

    # 4 ≠ 4 is False — the falsification condition was NOT met
    assert eval_result is False

    # --- Step 5: Full falsify gives SURVIVED ---
    result = falsify(truth, evidence)
    assert result.verdict == Verdict.SURVIVED
    assert result.form is not None
    assert result.evidence is evidence
    assert len(result.trace) > 0


def test_falsification_audit_claim_killed():
    """Same claim, but evidence says result is 5. Claim is killed."""

    truth = Analytic(statement="2 + 2 equals 4", lhs="result", rhs=4)
    evidence = Evidence(bindings={"result": 5})

    # Falsification asks: result ≠ 4?
    # With result=5: 5 ≠ 4 is True — falsification succeeded
    result = falsify(truth, evidence)

    assert result.verdict == Verdict.KILLED


def test_falsification_audit_missing_evidence():
    """No evidence provided. Verdict is UNCERTAIN."""

    truth = Analytic(statement="2 + 2 equals 4", lhs="result", rhs=4)
    evidence = Evidence(bindings={})

    result = falsify(truth, evidence)

    assert result.verdict == Verdict.UNCERTAIN
    assert "result" in result.reasoning


def test_falsification_audit_falsification_form_check():
    """FalsificationForm.check() works independently of the engine."""

    truth = Analytic(statement="2 + 2 equals 4", lhs="result", rhs=4)
    form = truth.falsify()

    # Direct check — bypasses the engine entirely
    assert form.check(result=4) is False  # 4 ≠ 4 → False
    assert form.check(result=5) is True   # 5 ≠ 4 → True


def test_falsification_audit_verdict_str():
    """VerdictResult has a human-readable string."""

    truth = Analytic(statement="2 + 2 equals 4", lhs="result", rhs=4)
    evidence = Evidence(bindings={"result": 4})
    result = falsify(truth, evidence)

    output = str(result)
    assert "SURVIVED" in output
    assert "result" in output
