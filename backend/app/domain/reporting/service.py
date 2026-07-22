"""Application service for the Reporting domain."""

from __future__ import annotations

from .report import Report
from .repository import ReportRepository
from .value_objects import ConfidenceScore
from .page import ReportPage
from .query import ReportQuery


class ReportService:
    """
    Coordinates report-related business operations.
    """

    def __init__(self, repository: ReportRepository) -> None:
        self._repository = repository

    def submit_report(self, report: Report) -> Report:
        """
        Submit a new report.

        Version 1 assigns an initial confidence score and
        persists the report.
        """
        report.assign_confidence(ConfidenceScore(0.5))

        return self._repository.save(report)

    def get_report(self, report_id):
        """Retrieve a report by its identifier."""
        return self._repository.get_by_id(report_id)

    def list_reports(
            self,
            query: ReportQuery,
        )-> ReportPage:
        """Retrieve reports matching a query."""
        return self._repository.list(query)