"""Schemas for AI report analysis."""

from pydantic import BaseModel

from app.domain.analysis.enums import SeverityLevel


class ReportAnalysisResponse(BaseModel):
    """
    AI-generated analysis returned to clients.
    """

    severity: SeverityLevel

    summary: str

    evidence: list[str]

    recommended_actions: list[str]

    confidence: float