"""Domain entity representing a submitted incident report."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.analysis.enums import SeverityLevel
from app.domain.reporting.enums import ReportStatus, ReportType
from app.domain.reporting.value_objects import (
    ConfidenceScore,
    GeoLocation,
    ObservationTime,
)


class Report:
    """
    Core domain entity for power grid incident reports.
    """

    def __init__(
        self,
        report_type: ReportType,
        location: GeoLocation,
        observed_at: ObservationTime,
        description: str,
        id: UUID | None = None,
        status: ReportStatus = ReportStatus.SUBMITTED,
        confidence_score: ConfidenceScore | None = None,
        submitted_at: datetime | None = None,
        reporter_id: UUID | None = None,
        severity: SeverityLevel | None = None,
        state: str | None = None,
        lga: str | None = None,
        landmark: str | None = None,
        reporter_phone: str | None = None,
    ) -> None:
        self.id = id or uuid4()
        self.report_type = report_type
        self.location = location
        self.observed_at = observed_at
        self.description = description
        self.status = status
        self.confidence_score = confidence_score or ConfidenceScore(0.5)
        self.submitted_at = submitted_at or datetime.now(timezone.utc)
        self.reporter_id = reporter_id
        self.severity = severity or SeverityLevel.LOW
        self.state = state
        self.lga = lga
        self.landmark = landmark
        self.reporter_phone = reporter_phone

    def assign_confidence(self, confidence: ConfidenceScore) -> None:
        """Assign a new confidence score to the report."""
        self.confidence_score = confidence

    def assign_severity(self, severity: SeverityLevel) -> None:
        """Assign an AI severity assessment to the report."""
        self.severity = severity