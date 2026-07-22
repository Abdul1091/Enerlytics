from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.api.schemas.report import ReportResponse
from app.domain.reporting.enums import (
    ReportStatus,
    ReportType,
)


class ReportQueryParams(BaseModel):

    status: ReportStatus | None = None

    report_type: ReportType | None = None

    reporter_id: UUID | None = None

    observed_from: datetime | None = None
    observed_to: datetime | None = None

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )

    offset: int = Field(
        default=0,
        ge=0,
    )

    sort_by: str = "submitted_at"

    descending: bool = True

class ReportPageResponse(BaseModel):
    items: list[ReportResponse]
    total: int
    limit: int
    offset: int