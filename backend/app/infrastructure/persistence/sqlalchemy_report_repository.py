"""SQLAlchemy implementation of the ReportRepository."""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy import String, func
from sqlalchemy.orm import Session

from app.db.mappers.report_mapper import DatabaseReportMapper
from app.db.models.report import ReportModel
from app.domain.reporting.page import ReportPage
from app.domain.reporting.query import ReportQuery
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

    def get_dashboard_stats(self) -> dict:
        """
        Compute real-time aggregate statistics for the dashboard.
        """
        # 1. Total Count
        total_reports = self._session.query(func.count(ReportModel.id)).scalar() or 0

        # 2. Status Counts
        status_rows = (
            self._session.query(
                ReportModel.status, 
                func.count(ReportModel.id)
            )
            .group_by(ReportModel.status)
            .all()
        )

        status_counts = {}
        for st, count in status_rows:
            if st is not None:
                key = str(st.value if hasattr(st, "value") else st).lower()
                status_counts[key] = count

        pending_count = (
            status_counts.get("submitted", 0)
            + status_counts.get("under_review", 0)
            + status_counts.get("pending", 0)
        )
        resolved_count = status_counts.get("resolved", 0)
        verified_count = status_counts.get("validated", 0) or status_counts.get("verified", 0)
        rejected_count = status_counts.get("rejected", 0)

        # 3. Average AI Confidence Score
        avg_confidence = self._session.query(
            func.avg(ReportModel.confidence_score)
        ).scalar() or 0.0

        # 4. Report Type Distribution
        type_rows = (
            self._session.query(
                ReportModel.report_type, 
                func.count(ReportModel.id)
            )
            .group_by(ReportModel.report_type)
            .all()
        )
        
        type_distribution = {}
        for r_type, count in type_rows:
            if r_type is not None:
                key = str(r_type.value if hasattr(r_type, "value") else r_type).lower()
                type_distribution[key] = count

        # 5. Report Severity Distribution
        severity_rows = (
            self._session.query(
                ReportModel.severity, 
                func.count(ReportModel.id)
            )
            .group_by(ReportModel.severity)
            .all()
        )

        severity_distribution = {}
        for sev, count in severity_rows:
            if sev is not None:
                key = str(sev.value if hasattr(sev, "value") else sev).lower()
                severity_distribution[key] = count
            else:
                severity_distribution["low"] = severity_distribution.get("low", 0) + count

        return {
            "total_reports": total_reports,
            "pending_count": pending_count,
            "resolved_count": resolved_count,
            "verified_count": verified_count,
            "rejected_count": rejected_count,
            "avg_confidence_score": round(float(avg_confidence) * 100, 1) if avg_confidence else 0.0,
            "type_distribution": type_distribution,
            "severity_distribution": severity_distribution,
        }

    def get_incident_trends(self, days: int = 7) -> list[dict]:
        """
        Groups total and critical report counts by date for the last N days.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        total_results = (
            self._session.query(
                func.date(ReportModel.submitted_at).label("trend_date"),
                func.count(ReportModel.id).label("count")
            )
            .filter(ReportModel.submitted_at >= cutoff_date)
            .group_by(func.date(ReportModel.submitted_at))
            .all()
        )

        critical_results = (
            self._session.query(
                func.date(ReportModel.submitted_at).label("trend_date"),
                func.count(ReportModel.id).label("count")
            )
            .filter(
                ReportModel.submitted_at >= cutoff_date,
                func.lower(func.cast(ReportModel.severity, String)).in_(["critical", "high"])
            )
            .group_by(func.date(ReportModel.submitted_at))
            .all()
        )

        total_counts = {str(r.trend_date): r.count for r in total_results}
        critical_counts = {str(r.trend_date): r.count for r in critical_results}

        trend_data = []
        for i in range(days - 1, -1, -1):
            day_date = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
            trend_data.append({
                "date": day_date,
                "total": total_counts.get(day_date, 0),
                "critical": critical_counts.get(day_date, 0)
            })

        return trend_data