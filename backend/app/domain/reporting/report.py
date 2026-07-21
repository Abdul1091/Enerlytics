"""Report entity for the Reporting domain."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from .enums import ReportStatus, ReportType
from .exceptions import InvalidReportStatusTransitionError
from .value_objects import (
    ConfidenceScore,
    GeoLocation,
    ObservationTime,
)


@dataclass(slots=True)
class Report:
    """
    Represents an electricity-related observation submitted to Enerlytics.

    A report begins as an unverified observation and progresses through
    validation as supporting evidence becomes available.
    """

    report_type: ReportType
    location: GeoLocation
    observed_at: ObservationTime
    description: str

    id: UUID = field(default_factory=uuid4)
    status: ReportStatus = field(default=ReportStatus.SUBMITTED)
    confidence_score: ConfidenceScore = field(
        default_factory=lambda: ConfidenceScore(0.0)
    )
    submitted_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    reporter_id: UUID | None = None

    def start_review(self) -> None:
        """Move the report into review."""
        self._transition(
            ReportStatus.SUBMITTED,
            ReportStatus.UNDER_REVIEW,
        )

    def validate(self) -> None:
        """Mark the report as validated."""
        self._transition(
            ReportStatus.UNDER_REVIEW,
            ReportStatus.VALIDATED,
        )

    def reject(self) -> None:
        """Reject the report."""
        self._transition(
            ReportStatus.UNDER_REVIEW,
            ReportStatus.REJECTED,
        )

    def resolve(self) -> None:
        """Mark the report as resolved."""
        self._transition(
            ReportStatus.VALIDATED,
            ReportStatus.RESOLVED,
        )

    def assign_confidence(
        self,
        confidence: ConfidenceScore,
    ) -> None:
        """
        Assign a confidence score to the report.
        """
        self.confidence_score = confidence

    def _transition(
        self,
        expected: ReportStatus,
        target: ReportStatus,
    ) -> None:
        """
        Perform a validated status transition.
        """
        if self.status != expected:
            raise InvalidReportStatusTransitionError(
                f"Cannot transition from "
                f"{self.status.value!r} "
                f"to {target.value!r}."
            )

        self.status = target