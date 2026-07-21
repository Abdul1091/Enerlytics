"""Mapper between the Reporting domain and API schemas."""

from __future__ import annotations

from app.api.schemas.report import ReportResponse
from app.domain.reporting.report import Report


class APIReportMapper:
    """
    Converts domain Report objects into API response schemas.

    This mapper isolates the API layer from the domain model,
    ensuring that HTTP responses remain independent of business
    objects.
    """

    @staticmethod
    def from_domain(report: Report) -> ReportResponse:
        """
        Convert a domain Report into a ReportResponse schema.
        """
        return ReportResponse(
            id=report.id,
            report_type=report.report_type,
            latitude=report.location.latitude,
            longitude=report.location.longitude,
            description=report.description,
            observed_at=report.observed_at.value,
            submitted_at=report.submitted_at,
            status=report.status,
            confidence_score=report.confidence_score.value,
            reporter_id=report.reporter_id,
        )