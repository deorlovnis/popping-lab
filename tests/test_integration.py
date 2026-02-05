"""Integration tests for the complete Veritas workflow."""

from __future__ import annotations

from veritas import (
    Analytic,
    Empirical,
    Evidence,
    Modal,
    Probabilistic,
    Verdict,
    claim,
    empirical,
    equality,
    invariant,
    probabilistic,
    sym,
    verified,
    verify,
)
from veritas.extensions import (
    DataGrounding,
    HTTPResponse,
    InvariantCheck,
    ModelAccuracy,
)


class TestAnalyticWorkflow:
    """Integration tests for Analytic claims."""

    def test_simple_equality_survives(self) -> None:
        """Test 2+2=4 workflow."""
        # Define claim
        truth = Analytic(
            statement="add(2,2) equals 4",
            lhs="result",
            rhs=4,
        )

        # Gather evidence
        actual_result = 2 + 2
        evidence = Evidence(
            bindings={"result": actual_result, "x": actual_result},
            source="direct computation",
        )

        # Verify
        result = verify(truth, evidence)
        assert result.verdict == Verdict.SURVIVED
        assert len(result.trace) > 0

    def test_simple_equality_killed(self) -> None:
        """Test failing equality claim."""
        truth = Analytic(
            statement="buggy_add(2,2) equals 4",
            lhs="result",
            rhs=4,
        )

        # Simulate buggy function
        buggy_result = 5
        evidence = Evidence(
            bindings={"result": buggy_result, "x": buggy_result},
        )

        result = verify(truth, evidence)
        assert result.verdict == Verdict.KILLED


class TestClaimContextManager:
    """Integration tests for claim() context manager."""

    def test_claim_survives(self) -> None:
        """claim() context manager with surviving claim."""
        with claim(Analytic("2+2=4", lhs="result", rhs=4)) as c:
            c.bind(result=2 + 2, x=4)

        assert c.result is not None
        assert c.result.verdict == Verdict.SURVIVED

    def test_claim_killed(self) -> None:
        """claim() context manager with killed claim."""
        with claim(Analytic("2+2=5", lhs="result", rhs=5)) as c:
            c.bind(result=4, x=4)  # 2+2=4, not 5

        assert c.result is not None
        assert c.result.verdict == Verdict.KILLED

    def test_claim_observe(self) -> None:
        """claim() context manager with observe()."""
        with claim(Analytic("computation works", lhs="result", rhs=10)) as c:
            value = c.observe("intermediate", 5)
            c.bind(result=value * 2, x=10)

        assert c.evidence.bindings["intermediate"] == 5
        assert c.result is not None
        assert c.result.verdict == Verdict.SURVIVED


class TestVerifiedDecorator:
    """Integration tests for @verified decorator."""

    def test_verified_survives(self) -> None:
        """@verified decorator with surviving claim."""

        @verified(lambda: Analytic("square root", lhs="result", rhs=4))
        def test_sqrt() -> dict[str, int]:
            import math

            return {"result": int(math.sqrt(16)), "x": 4}

        result = test_sqrt()
        assert result.verdict == Verdict.SURVIVED

    def test_verified_single_return(self) -> None:
        """@verified decorator with single return value."""

        @verified(lambda: Analytic("multiply", lhs="result", rhs=6))
        def test_multiply() -> dict[str, int]:
            return {"result": 2 * 3, "x": 6}

        result = test_multiply()
        assert result.verdict == Verdict.SURVIVED


class TestBuilderFunctions:
    """Tests for convenience builder functions."""

    def test_equality_builder(self) -> None:
        """equality() creates Analytic truth."""
        t = equality("2+2=4", lhs="result", rhs=4)
        assert isinstance(t, Analytic)
        assert t.rhs == 4

    def test_invariant_builder(self) -> None:
        """invariant() creates Modal truth."""
        x = sym("x")
        t = invariant("x >= 0", predicate=x >= 0)
        assert isinstance(t, Modal)

    def test_empirical_builder(self) -> None:
        """empirical() creates Empirical truth."""
        t = empirical("API works", observation_var="status", expected=lambda s: s == 200)
        assert isinstance(t, Empirical)

    def test_probabilistic_builder(self) -> None:
        """probabilistic() creates Probabilistic truth."""
        t = probabilistic("accuracy > 50%", metric="acc", threshold=0.5, direction=">")
        assert isinstance(t, Probabilistic)


class TestEmpiricalWorkflow:
    """Integration tests for Empirical claims."""

    def test_api_status_survives(self) -> None:
        """Empirical claim about API status."""
        truth = Empirical(
            statement="API returns 200",
            observation_var="status",
            expected_predicate=lambda s: s == 200,
        )

        # Simulate API call
        status = 200
        satisfied = truth.check_observation(status)
        assert satisfied is True

    def test_api_status_killed(self) -> None:
        """Empirical claim killed by observation."""
        truth = Empirical(
            statement="API returns 200",
            observation_var="status",
            expected_predicate=lambda s: s == 200,
        )

        # Simulate failed API call
        status = 404
        satisfied = truth.check_observation(status)
        assert satisfied is False


class TestProbabilisticWorkflow:
    """Integration tests for Probabilistic claims."""

    def test_accuracy_threshold_survives(self) -> None:
        """Probabilistic claim about model accuracy."""
        truth = Probabilistic(
            statement="Model accuracy > 60%",
            metric="accuracy",
            threshold=0.6,
            direction=">",
        )

        # Simulate model evaluation
        accuracy = 0.75
        satisfied = truth.check_threshold(accuracy)
        assert satisfied is True

    def test_accuracy_threshold_killed(self) -> None:
        """Probabilistic claim killed by low accuracy."""
        truth = Probabilistic(
            statement="Model accuracy > 60%",
            metric="accuracy",
            threshold=0.6,
            direction=">",
        )

        accuracy = 0.55
        satisfied = truth.check_threshold(accuracy)
        assert satisfied is False


class TestDomainExtensions:
    """Integration tests for domain extension classes."""

    def test_http_response_extension(self) -> None:
        """HTTPResponse domain extension."""
        ext = HTTPResponse(endpoint="/api/health", expected_status=200)
        truth = ext.to_base_truth()

        assert isinstance(truth, Analytic)
        assert "200" in truth.statement

        evidence = ext.bind(status_code=200)
        assert evidence.bindings["status_code"] == 200

    def test_model_accuracy_extension(self) -> None:
        """ModelAccuracy domain extension."""
        ext = ModelAccuracy(model_name="classifier", threshold=0.8)
        truth = ext.to_base_truth()

        assert isinstance(truth, Probabilistic)
        assert truth.threshold == 0.8

        evidence = ext.bind(accuracy=0.85, dataset="test")
        assert evidence.bindings["accuracy"] == 0.85
        assert evidence.metadata["dataset"] == "test"

    def test_data_grounding_extension(self) -> None:
        """DataGrounding domain extension."""
        ext = DataGrounding(claim="function works", evidence_type="test")
        truth = ext.to_base_truth()

        assert isinstance(truth, Empirical)

        evidence = ext.bind(support="test_function.py")
        assert evidence.bindings["support"] == "test_function.py"


class TestEndToEndScenarios:
    """End-to-end scenarios testing complete workflows."""

    def test_math_library_claim(self) -> None:
        """Test a claim about a math function."""
        import math

        with claim(equality("sqrt(16) = 4", lhs="result", rhs=4.0)) as c:
            result = math.sqrt(16)
            c.bind(result=result, x=result)

        assert c.result is not None
        assert c.result.verdict == Verdict.SURVIVED

    def test_string_operation_claim(self) -> None:
        """Test a claim about string operations."""
        # Use boolean equality check since strings can't be SymPy symbols
        with claim(equality("upper('hello') = 'HELLO'", lhs="result", rhs=True)) as c:
            result = "hello".upper() == "HELLO"
            c.bind(result=result, x=result)

        assert c.result is not None
        assert c.result.verdict == Verdict.SURVIVED

    def test_list_membership_claim(self) -> None:
        """Test a membership-style claim."""
        with claim(equality("3 in [1,2,3] is True", lhs="result", rhs=True)) as c:
            result = 3 in [1, 2, 3]
            c.bind(result=result, x=result)

        assert c.result is not None
        assert c.result.verdict == Verdict.SURVIVED

    def test_ordering_claim(self) -> None:
        """Test an ordering claim via equality."""
        with claim(equality("sorted list is sorted", lhs="result", rhs=True)) as c:
            data = [3, 1, 4, 1, 5]
            sorted_data = sorted(data)
            is_sorted = all(sorted_data[i] <= sorted_data[i + 1] for i in range(len(sorted_data) - 1))
            c.bind(result=is_sorted, x=is_sorted)

        assert c.result is not None
        assert c.result.verdict == Verdict.SURVIVED
