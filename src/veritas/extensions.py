"""Extension base classes for domain-specific truths.

This module provides abstract base classes for extending Veritas
to specific domains (e.g., web APIs, databases, ML models).

DomainTruth allows domain-specific claim types that convert to
base Veritas truth types for verification.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from .evidence import Evidence
from .truth import Analytic, Empirical, Modal, Probabilistic, Truth

if TYPE_CHECKING:
    pass


class DomainTruth(ABC):
    """Abstract base class for domain-specific truths.

    Subclass this to create domain-specific claim types that know how
    to convert themselves to base Veritas truth types.

    Example:
        >>> class APIEndpointReturns(DomainTruth):
        ...     domain = "api"
        ...
        ...     def __init__(self, endpoint: str, expected_status: int):
        ...         self.endpoint = endpoint
        ...         self.expected_status = expected_status
        ...
        ...     def to_base_truth(self) -> Analytic:
        ...         return Analytic(
        ...             statement=f"{self.endpoint} returns {self.expected_status}",
        ...             lhs="status_code",
        ...             rhs=self.expected_status,
        ...         )
        ...
        ...     def bind(self, response) -> Evidence:
        ...         return Evidence(bindings={"status_code": response.status_code})
    """

    domain: str = ""
    """The domain this truth type belongs to (e.g., 'api', 'db', 'ml')."""

    @abstractmethod
    def to_base_truth(self) -> Truth:
        """Convert this domain truth to a base Veritas truth type.

        Returns:
            One of: Analytic, Modal, Empirical, or Probabilistic
        """
        ...

    @abstractmethod
    def bind(self, *args: Any, **kwargs: Any) -> Evidence:
        """Create evidence from domain-specific data.

        Subclasses should implement this to extract relevant bindings
        from domain objects (e.g., HTTP responses, database results).

        Returns:
            Evidence with bindings extracted from the domain data
        """
        ...


# Example domain extensions


@dataclass
class HTTPResponse:
    """Domain truth for HTTP response assertions.

    Tests that an HTTP endpoint returns the expected status code.
    """

    endpoint: str
    """The HTTP endpoint being tested."""

    expected_status: int
    """The expected HTTP status code."""

    domain: str = "api"

    def to_base_truth(self) -> Analytic:
        """Convert to an Analytic truth about status code equality."""
        return Analytic(
            statement=f"GET {self.endpoint} returns {self.expected_status}",
            lhs="status_code",
            rhs=self.expected_status,
            var_name="response",
        )

    def bind(self, status_code: int, **metadata: Any) -> Evidence:
        """Create evidence from an HTTP response.

        Args:
            status_code: The actual status code received
            **metadata: Additional metadata (headers, body, etc.)

        Returns:
            Evidence with the status code binding
        """
        return Evidence(
            bindings={"status_code": status_code},
            source=f"HTTP {self.endpoint}",
            metadata=metadata,
        )


@dataclass
class ModelAccuracy:
    """Domain truth for ML model accuracy claims.

    Tests that a model achieves at least a threshold accuracy.
    """

    model_name: str
    """Name of the model being tested."""

    threshold: float
    """Minimum required accuracy (0.0 to 1.0)."""

    domain: str = "ml"

    def to_base_truth(self) -> Probabilistic:
        """Convert to a Probabilistic truth about accuracy threshold."""
        return Probabilistic(
            statement=f"{self.model_name} accuracy >= {self.threshold}",
            metric="accuracy",
            threshold=self.threshold,
            direction=">=",
        )

    def bind(self, accuracy: float, **metadata: Any) -> Evidence:
        """Create evidence from model evaluation.

        Args:
            accuracy: The measured accuracy
            **metadata: Additional metadata (dataset, split, etc.)

        Returns:
            Evidence with the accuracy binding
        """
        return Evidence(
            bindings={"accuracy": accuracy},
            source=f"model evaluation: {self.model_name}",
            metadata=metadata,
        )


@dataclass
class InvariantCheck:
    """Domain truth for state invariant assertions.

    Tests that a property holds after operations.
    """

    property_name: str
    """Human-readable name of the property."""

    predicate: Any
    """SymPy predicate that must hold."""

    domain: str = "state"

    def to_base_truth(self) -> Modal:
        """Convert to a Modal truth about invariant preservation."""
        return Modal(
            statement=f"{self.property_name} holds",
            invariant=self.predicate,
        )

    def bind(self, state: Any, predicate_result: bool) -> Evidence:
        """Create evidence from state check.

        Args:
            state: The state that was checked
            predicate_result: Whether the predicate held

        Returns:
            Evidence with state binding
        """
        return Evidence(
            bindings={"state": state, "holds": predicate_result},
            source=f"invariant check: {self.property_name}",
        )


@dataclass
class DataGrounding:
    """Domain truth for data grounding claims.

    Tests that a claim has supporting evidence/documentation.
    """

    claim: str
    """The claim that needs grounding."""

    evidence_type: str
    """Type of evidence expected (e.g., 'test', 'doc', 'citation')."""

    domain: str = "grounding"

    def to_base_truth(self) -> Empirical:
        """Convert to an Empirical truth about evidence existence."""
        return Empirical(
            statement=f"{self.claim} has {self.evidence_type} support",
            observation_var="support",
            expected_predicate=lambda s: s is not None and s != "",
            contradiction_description=f"No {self.evidence_type} found for: {self.claim}",
        )

    def bind(self, support: Any, **metadata: Any) -> Evidence:
        """Create evidence from grounding check.

        Args:
            support: The supporting evidence found (or None)
            **metadata: Additional metadata

        Returns:
            Evidence with support binding
        """
        return Evidence(
            bindings={"support": support},
            source=f"grounding check: {self.evidence_type}",
            metadata=metadata,
        )
