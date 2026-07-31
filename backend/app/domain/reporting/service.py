"""Application service for the Reporting domain."""

from __future__ import annotations

from uuid import UUID

from app.infrastructure.ai.analyzer import ReportAnalyzer

from .enums import ReportStatus
from .page import ReportPage
from .query import ReportQuery
from .report import Report
from .repository import ReportRepository
from .value_objects import ConfidenceScore


class ReportService:
    """
    Coordinates report-related business operations.
    """

    def __init__(
        self,
        repository: ReportRepository,
        analyzer: ReportAnalyzer | None = None,
    ) -> None:
        self._repository = repository
        self._analyzer = analyzer

    def submit_report(self, report: Report) -> Report:
        """
        Submit a new report.

        Executes heuristic AI analysis to calculate severity and
        confidence score before persistence.
        """
        if self._analyzer:
            analysis = self._analyzer.analyze(report)
            report.assign_severity(analysis.severity)
            report.assign_confidence(ConfidenceScore(analysis.confidence))

        return self._repository.save(report)

    def get_report(self, report_id: UUID) -> Report | None:
        """Retrieve a report by its identifier."""
        return self._repository.get_by_id(report_id)

    def list_reports(
        self,
        query: ReportQuery,
    ) -> ReportPage:
        """Retrieve reports matching a query."""
        return self._repository.list(query)

    def update_report_status(
        self,
        report_id: UUID,
        new_status: ReportStatus,
    ) -> Report:
        report = self._repository.get_by_id(report_id)
        if report is None:
            raise ValueError(f"Report with ID {report_id} not found.")

        report.status = new_status

        return self._repository.save(report)