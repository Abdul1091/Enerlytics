from app.api.schemas.report_analysis import (
    ReportAnalysisResponse,
)
from app.domain.analysis.report_analysis import (
    ReportAnalysis,
)


class ReportAnalysisMapper:

    @staticmethod
    def from_domain(
        analysis: ReportAnalysis,
    ) -> ReportAnalysisResponse:

        return ReportAnalysisResponse(
            severity=analysis.severity,
            summary=analysis.summary,
            evidence=analysis.evidence,
            recommended_actions=analysis.recommended_actions,
            confidence=analysis.confidence,
        )