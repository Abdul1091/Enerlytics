"""Mapper between the Reporting domain and SQLAlchemy persistence model."""

from __future__ import annotations

from app.db.models.report import ReportModel
from app.domain.reporting.report import Report
from app.domain.reporting.value_objects import (
    ConfidenceScore,
    GeoLocation,
    ObservationTime,
)


class DatabaseReportMapper:
    """
    Converts between domain Report objects and SQLAlchemy ReportModel objects.

    The mapper isolates persistence concerns from the domain model,
    ensuring that neither layer depends directly on the other.
    """

    @staticmethod
    def to_model(report: Report) -> ReportModel:
        """
        Convert a domain Report into a SQLAlchemy ReportModel.
        """
        return ReportModel(
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

    @staticmethod
    def to_domain(model: ReportModel) -> Report:
        """
        Convert a SQLAlchemy ReportModel into a domain Report.
        """
        return Report(
            id=model.id,
            report_type=model.report_type,
            location=GeoLocation(
                latitude=model.latitude,
                longitude=model.longitude,
            ),
            observed_at=ObservationTime(model.observed_at),
            description=model.description,
            status=model.status,
            confidence_score=ConfidenceScore(
                model.confidence_score,
            ),
            submitted_at=model.submitted_at,
            reporter_id=model.reporter_id,
        )