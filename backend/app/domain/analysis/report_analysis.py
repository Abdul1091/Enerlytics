from dataclasses import dataclass
from uuid import UUID

from app.domain.analysis.enums import SeverityLevel


@dataclass(slots=True)
class ReportAnalysis:
    """
    AI interpretation of a report.
    """

    report_id: UUID

    severity: SeverityLevel

    summary: str

    evidence: list[str]

    recommended_actions: list[str]

    confidence: float