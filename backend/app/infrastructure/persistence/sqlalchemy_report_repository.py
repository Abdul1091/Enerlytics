"""SQLAlchemy implementation of the ReportRepository."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.domain.reporting.page import ReportPage
from app.domain.reporting.query import ReportQuery
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

    def list(
        self,
        query: ReportQuery,
    ) -> ReportPage:
        """Retrieve reports matching a query."""

        stmt = self._session.query(ReportModel)

        if query.status is not None:
            stmt = stmt.filter(
                ReportModel.status == query.status
            )

        if query.report_type is not None:
            stmt = stmt.filter(
                ReportModel.report_type == query.report_type
            )

        if query.reporter_id is not None:
            stmt = stmt.filter(
                ReportModel.reporter_id == query.reporter_id
            )

        if query.observed_from is not None:
            stmt = stmt.filter(
                ReportModel.observed_at >= query.observed_from
            )

        if query.observed_to is not None:
            stmt = stmt.filter(
                ReportModel.observed_at <= query.observed_to
            )

        total = stmt.order_by(None).count()

        sort_columns = {
            "submitted_at": ReportModel.submitted_at,
            "observed_at": ReportModel.observed_at,
            "confidence_score": ReportModel.confidence_score,
        }

        column = sort_columns.get(
            query.sort_by,
            ReportModel.submitted_at,
        )

        stmt = stmt.order_by(
            column.desc()
            if query.descending
            else column.asc()
        )

        stmt = stmt.offset(query.offset).limit(query.limit)

        reports = [
            DatabaseReportMapper.to_domain(model)
            for model in stmt.all()
        ]

        return ReportPage(
            items=reports,
            total=total,
            limit=query.limit,
            offset=query.offset,
        )

    def delete(self, report_id: UUID) -> None:
        """
        Delete a report.
        """
        model = self._session.get(ReportModel, report_id)

        if model is None:
            return

        self._session.delete(model)
        self._session.commit()