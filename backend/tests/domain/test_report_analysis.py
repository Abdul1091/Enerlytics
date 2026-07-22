"""Tests for ReportAnalysis."""

from uuid import uuid4

from app.domain.analysis.enums import SeverityLevel
from app.domain.analysis.report_analysis import (
    ReportAnalysis,
)


def test_report_analysis_creation():
    report = ReportAnalysis(
        report_id=uuid4(),
        severity=SeverityLevel.MEDIUM,
        summary="summary",
        evidence=["evidence"],
        recommended_actions=["action"],
        confidence=0.75,
    )

    assert report.severity == SeverityLevel.MEDIUM
    assert report.summary == "summary"
    assert report.evidence == ["evidence"]
    assert report.recommended_actions == [
        "action"
    ]
    assert report.confidence == 0.75