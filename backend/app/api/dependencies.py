"""Dependency providers."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domain.reporting.service import ReportService
from app.infrastructure.persistence.sqlalchemy_report_repository import (
    SQLAlchemyReportRepository,
)

from app.infrastructure.ai.analyzer import ReportAnalyzer
from app.infrastructure.ai.heuristic_analyzer import (
    RuleBasedReportAnalyzer,
)


def get_report_service(
    db: Annotated[Session, Depends(get_db)],
) -> ReportService:
    return ReportService(
        SQLAlchemyReportRepository(db)
    )


def get_report_analyzer() -> ReportAnalyzer:
    """
    Return the configured AI report analyzer.
    """
    return RuleBasedReportAnalyzer()