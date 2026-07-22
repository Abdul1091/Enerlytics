# backend/app/infrastructure/ai/heuristic_analyzer.py
from __future__ import annotations

from app.domain.analysis.enums import SeverityLevel
from app.domain.analysis.report_analysis import ReportAnalysis
from app.domain.reporting.report import Report
from app.infrastructure.ai.analyzer import ReportAnalyzer


class RuleBasedReportAnalyzer(ReportAnalyzer):
    """
    Intelligent analysis engine combining keyword heuristics,
    severity scoring, and XAI evidence generation.
    """

    CRITICAL_KEYWORDS = {
        "explosion",
        "exploded",
        "fire",
        "burning",
        "sparks",
        "sparking",
        "fallen cable",
        "wire on ground",
        "live wire",
        "electrocution",
    }
    HIGH_KEYWORDS = {
        "blackout",
        "power outage",
        "no electricity",
        "no power",
        "total darkness",
        "substation",
        "feeder",
        "transformer",
    }
    MEDIUM_KEYWORDS = {
        "low voltage",
        "voltage is low",
        "voltage low",
        "fluctuating",
        "fluctuation",
        "dim lights",
        "dim light",
        "phase fault",
        "single phase",
    }

    def analyze(self, report: Report) -> ReportAnalysis:
        desc_lower = report.description.lower()
        evidence: list[str] = []
        recommended_actions: list[str] = []

        # Keywords Analysis & Evidence Gathering
        matched_critical = [kw for kw in self.CRITICAL_KEYWORDS if kw in desc_lower]
        matched_high = [kw for kw in self.HIGH_KEYWORDS if kw in desc_lower]
        matched_medium = [kw for kw in self.MEDIUM_KEYWORDS if kw in desc_lower]

        score = 0

        score += len(matched_medium)
        score += len(matched_high) * 2
        score += len(matched_critical) * 3

        if score >= 3:
            severity = SeverityLevel.CRITICAL
            confidence = 0.95
            evidence.append(f"Safety hazard detected: matched terms {matched_critical}")
            recommended_actions.append("Dispatch emergency technical field team immediately.")
            recommended_actions.append("Isolate local feeder branch to prevent electrical shock/fire.")

        elif score >= 2:
            severity = SeverityLevel.HIGH
            confidence = 0.85
            evidence.append(f"Grid disruption identified: matched terms {matched_high}")
            recommended_actions.append("Verify primary substation status with DisCo operator.")
            recommended_actions.append("Notify regional control center for load redistribution.")

        elif score >= 1:
            severity = SeverityLevel.MEDIUM
            confidence = 0.75
            evidence.append(f"Power quality issue detected: matched terms {matched_medium}")
            recommended_actions.append("Schedule distribution transformer load balancing test.")

        else:
            severity = SeverityLevel.LOW
            confidence = 0.60
            evidence.append("Standard citizen observation with no high-risk trigger words.")
            recommended_actions.append("Log observation for routine DisCo queue inspection.")

        # XAI Explanation Summary
        summary = (
            f"AI Severity Assessment: {severity.value.upper()} "
            f"(Confidence: {int(confidence * 100)}%). {evidence[0]}"
        )

        return ReportAnalysis(
            report_id=report.id,
            severity=severity,
            summary=summary,
            evidence=evidence,
            recommended_actions=recommended_actions,
            confidence=confidence,
        )