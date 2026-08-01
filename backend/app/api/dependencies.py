"""Dependency providers."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domain.reporting.service import ReportService
from app.infrastructure.ai.analyzer import ReportAnalyzer
from app.infrastructure.ai.heuristic_analyzer import (
    RuleBasedReportAnalyzer,
)
from app.infrastructure.persistence.sqlalchemy_report_repository import (
    SQLAlchemyReportRepository,
)


def get_report_analyzer() -> ReportAnalyzer:
    """
    Return the configured AI report analyzer.
    """
    return RuleBasedReportAnalyzer()


def get_report_service(
    db: Annotated[Session, Depends(get_db)],
    analyzer: Annotated[ReportAnalyzer, Depends(get_report_analyzer)],
) -> ReportService:
    """
    Construct the ReportService with repository and analyzer dependencies.
    """
    return ReportService(
        repository=SQLAlchemyReportRepository(db),
        analyzer=analyzer,
    )