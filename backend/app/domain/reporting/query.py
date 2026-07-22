from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .enums import ReportStatus, ReportType


@dataclass(slots=True)
class ReportQuery:
    status: ReportStatus | None = None
    report_type: ReportType | None = None

    reporter_id: UUID | None = None

    observed_from: datetime | None = None
    observed_to: datetime | None = None

    limit: int = 20
    offset: int = 0

    sort_by: str = "submitted_at"
    descending: bool = True