from abc import ABC, abstractmethod

from app.domain.reporting.report import Report
from app.domain.analysis.report_analysis import ReportAnalysis


class ReportAnalyzer(ABC):

    @abstractmethod
    def analyze(
        self,
        report: Report,
    ) -> ReportAnalysis:
        """
        Produce an AI assessment for a report.
        """