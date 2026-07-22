from app.api.schemas.report_query import ReportQueryParams
from app.domain.reporting.query import ReportQuery


class ReportQueryMapper:

    @staticmethod
    def to_domain(
        params: ReportQueryParams,
    ) -> ReportQuery:

        return ReportQuery(
            status=params.status,
            report_type=params.report_type,
            reporter_id=params.reporter_id,
            observed_from=params.observed_from,
            observed_to=params.observed_to,
            limit=params.limit,
            offset=params.offset,
            sort_by=params.sort_by,
            descending=params.descending,
        )