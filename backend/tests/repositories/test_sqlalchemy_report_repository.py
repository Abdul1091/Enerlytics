"""Tests for the SQLAlchemyReportRepository."""

from __future__ import annotations

from uuid import uuid4

from app.domain.reporting.enums import ReportStatus


def test_save_report(repository, report):
    """
    Saving a report should persist it.
    """
    saved = repository.save(report)

    assert saved.id == report.id
    assert saved.description == report.description
    assert saved.location.latitude == report.location.latitude
    assert saved.location.longitude == report.location.longitude
    assert saved.status == ReportStatus.SUBMITTED


def test_get_existing_report(repository, report):
    """
    Repository should retrieve a saved report.
    """
    repository.save(report)

    retrieved = repository.get_by_id(report.id)

    assert retrieved is not None
    assert retrieved.id == report.id
    assert retrieved.description == report.description
    assert retrieved.report_type == report.report_type


def test_get_unknown_report_returns_none(repository):
    """
    Unknown report IDs should return None.
    """
    report = repository.get_by_id(uuid4())

    assert report is None


def test_list_reports(repository, report):
    """
    Repository should list saved reports.
    """
    repository.save(report)

    reports = repository.list()

    assert len(reports) == 1
    assert reports[0].id == report.id


def test_delete_report(repository, report):
    """
    Deleted reports should no longer exist.
    """
    repository.save(report)

    repository.delete(report.id)

    assert repository.get_by_id(report.id) is None


def test_update_existing_report(repository, report):
    """
    Saving an existing report should update it.
    """
    repository.save(report)

    report.start_review()
    repository.save(report)

    updated = repository.get_by_id(report.id)

    assert updated is not None
    assert updated.status == ReportStatus.UNDER_REVIEW


def test_multiple_reports(repository, report):
    """
    Repository should persist multiple reports.
    """
    repository.save(report)

    second = report.__class__(
        report_type=report.report_type,
        location=report.location,
        observed_at=report.observed_at,
        description="Transformer exploded.",
    )

    repository.save(second)

    reports = repository.list()

    assert len(reports) == 2