"""Pydantic schemas for the Reporting API."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.reporting.enums import ReportStatus, ReportType


class ReportCreate(BaseModel):
    """
    Request body for creating a report.
    """

    report_type: ReportType

    latitude: float = Field(
        ge=-90,
        le=90,
        description="Latitude of the observation.",
    )

    longitude: float = Field(
        ge=-180,
        le=180,
        description="Longitude of the observation.",
    )

    description: str = Field(
        min_length=5,
        max_length=5000,
    )

    observed_at: datetime

    reporter_id: UUID | None = None


class ReportResponse(BaseModel):
    """
    Response returned after creating or retrieving a report.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID

    report_type: ReportType

    latitude: float

    longitude: float

    description: str

    observed_at: datetime

    submitted_at: datetime

    status: ReportStatus

    confidence_score: float

    reporter_id: UUID | None