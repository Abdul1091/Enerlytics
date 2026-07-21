"""SQLAlchemy implementation of the ReportRepository."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.mappers.report_mapper import DatabaseReportMapper
from app.db.models.report import ReportModel
from app.domain.reporting.report import Report
from app.domain.reporting.repository import ReportRepository


class SQLAlchemyReportRepository(ReportRepository):
    """
    SQLAlchemy implementation of the ReportRepository.

    Responsible only for persistence. It delegates all business
    rules to the domain layer and all object translation to the
    ReportMapper.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, report: Report) -> Report:
        """
        Persist a report.

        If the report already exists, SQLAlchemy's merge() updates it.
        Otherwise, it inserts a new record.
        """
        model = DatabaseReportMapper.to_model(report)

        persisted = self._session.merge(model)

        self._session.commit()
        self._session.refresh(persisted)

        return DatabaseReportMapper.to_domain(persisted)

    def get_by_id(self, report_id: UUID) -> Report | None:
        """
        Retrieve a report by its identifier.
        """
        model = self._session.get(ReportModel, report_id)

        if model is None:
            return None

        return DatabaseReportMapper.to_domain(model)

    def list(self) -> list[Report]:
        """
        Retrieve all reports.
        """
        models = self._session.query(ReportModel).all()

        return [
            DatabaseReportMapper.to_domain(model)
            for model in models
        ]

    def delete(self, report_id: UUID) -> None:
        """
        Delete a report.
        """
        model = self._session.get(ReportModel, report_id)

        if model is None:
            return

        self._session.delete(model)
        self._session.commit()