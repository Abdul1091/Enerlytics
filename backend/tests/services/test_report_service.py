"""Tests for the ReportService."""

from __future__ import annotations

from uuid import UUID, uuid4

import pytest

from app.domain.reporting.report import Report
from app.domain.reporting.repository import ReportRepository
from app.domain.reporting.service import ReportService


class FakeReportRepository(ReportRepository):
    """In-memory repository for service tests."""

    def __init__(self):
        self._reports: dict[UUID, Report] = {}

    def save(self, report: Report) -> Report:
        self._reports[report.id] = report
        return report

    def get_by_id(self, report_id: UUID) -> Report | None:
        return self._reports.get(report_id)

    def list(self) -> list[Report]:
        return list(self._reports.values())
    
    def delete(self, report_id: UUID) -> None:
        """Implement the required abstract delete method."""
        self._reports.pop(report_id, None)


@pytest.fixture
def repository():
    return FakeReportRepository()


@pytest.fixture
def service(repository):
    return ReportService(repository)


def test_submit_report_assigns_default_confidence(
    service,
    report,
):
    saved = service.submit_report(report)

    assert saved.confidence_score.value == 0.5


def test_submit_report_persists_report(
    service,
    repository,
    report,
):
    service.submit_report(report)

    persisted = repository.get_by_id(report.id)

    assert persisted is not None
    assert persisted.id == report.id


def test_get_existing_report(
    service,
    repository,
    report,
):
    repository.save(report)

    found = service.get_report(report.id)

    assert found == report


def test_get_unknown_report(
    service,
):
    assert service.get_report(uuid4()) is None


def test_list_reports(
    service,
    repository,
    report,
):
    repository.save(report)

    reports = service.list_reports()

    assert len(reports) == 1
    assert reports[0] == report