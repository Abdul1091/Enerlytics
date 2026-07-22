"""Tests for the rule-based AI report analyzer."""

from app.domain.analysis.enums import SeverityLevel
from app.infrastructure.ai.heuristic_analyzer import (
    RuleBasedReportAnalyzer,
)


def test_detects_low_severity(report):
    report.description = "Street light has been off for two days."

    analysis = RuleBasedReportAnalyzer().analyze(report)

    assert analysis.severity == SeverityLevel.LOW
    assert analysis.confidence == 0.60


def test_detects_medium_severity(report):
    report.description = (
        "Residents are experiencing low voltage."
    )

    analysis = RuleBasedReportAnalyzer().analyze(report)

    assert analysis.severity == SeverityLevel.MEDIUM
    assert analysis.confidence == 0.75


def test_detects_high_severity(report):
    report.description = (
        "Entire community has blackout after feeder trip."
    )

    analysis = RuleBasedReportAnalyzer().analyze(report)

    assert analysis.severity == SeverityLevel.HIGH
    assert analysis.confidence == 0.85


def test_detects_critical_severity(report):
    report.description = (
        "Transformer explosion with sparks."
    )

    analysis = RuleBasedReportAnalyzer().analyze(report)

    assert analysis.severity == SeverityLevel.CRITICAL
    assert analysis.confidence == 0.95


def test_generates_summary(report):
    report.description = "Low voltage."

    analysis = RuleBasedReportAnalyzer().analyze(report)

    assert "AI Severity Assessment" in analysis.summary


def test_generates_evidence(report):
    report.description = (
        "Transformer explosion."
    )

    analysis = RuleBasedReportAnalyzer().analyze(report)

    assert len(analysis.evidence) > 0


def test_generates_recommended_actions(report):
    report.description = (
        "Transformer explosion."
    )

    analysis = RuleBasedReportAnalyzer().analyze(report)

    assert len(analysis.recommended_actions) > 0


def test_confidence_is_valid(report):
    analysis = RuleBasedReportAnalyzer().analyze(report)

    assert 0.0 <= analysis.confidence <= 1.0