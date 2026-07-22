"""Tests for the report analysis mapper."""

from uuid import uuid4

from app.api.mappers.report_analysis_mapper import (
    ReportAnalysisMapper,
)
from app.domain.analysis.enums import SeverityLevel
from app.domain.analysis.report_analysis import (
    ReportAnalysis,
)


def test_from_domain():
    analysis = ReportAnalysis(
        report_id=uuid4(),
        severity=SeverityLevel.HIGH,
        summary="High severity.",
        evidence=["blackout"],
        recommended_actions=["Dispatch team"],
        confidence=0.9,
    )

    response = ReportAnalysisMapper.from_domain(
        analysis
    )

    assert response.severity == SeverityLevel.HIGH
    assert response.summary == "High severity."
    assert response.evidence == ["blackout"]
    assert response.recommended_actions == [
        "Dispatch team"
    ]
    assert response.confidence == 0.9