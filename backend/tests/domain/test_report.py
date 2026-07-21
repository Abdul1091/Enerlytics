"""Tests for Report."""

import pytest

from app.domain.reporting.enums import ReportStatus
from app.domain.reporting.exceptions import (
    InvalidReportStatusTransitionError,
)
from app.domain.reporting.value_objects import ConfidenceScore


def test_default_status(report):
    assert report.status == ReportStatus.SUBMITTED


def test_default_confidence(report):
    assert report.confidence_score.value == 0.0


def test_start_review(report):
    report.start_review()

    assert report.status == ReportStatus.UNDER_REVIEW


def test_validate(report):
    report.start_review()
    report.validate()

    assert report.status == ReportStatus.VALIDATED


def test_resolve(report):
    report.start_review()
    report.validate()
    report.resolve()

    assert report.status == ReportStatus.RESOLVED


def test_reject(report):
    report.start_review()
    report.reject()

    assert report.status == ReportStatus.REJECTED


def test_invalid_transition(report):
    with pytest.raises(
        InvalidReportStatusTransitionError,
    ):
        report.resolve()


def test_assign_confidence(report):
    report.assign_confidence(
        ConfidenceScore(0.92)
    )

    assert report.confidence_score.value == 0.92