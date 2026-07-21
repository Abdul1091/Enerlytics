"""Reporting API routes."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_report_service
from app.api.schemas.report import (
    ReportCreate,
    ReportResponse,
)
from app.domain.reporting.report import Report
from app.domain.reporting.service import ReportService
from app.domain.reporting.value_objects import (
    GeoLocation,
    ObservationTime,
)

from app.api.mappers import APIReportMapper

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.post(
    "",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_report(
    payload: ReportCreate,
    service: Annotated[
        ReportService,
        Depends(get_report_service),
    ],
):
    report = Report(
        report_type=payload.report_type,
        location=GeoLocation(
            payload.latitude,
            payload.longitude,
        ),
        observed_at=ObservationTime(
            payload.observed_at,
        ),
        description=payload.description,
        reporter_id=payload.reporter_id,
    )

    report = service.submit_report(report)

    return APIReportMapper.from_domain(report)


@router.get(
    "/{report_id}",
    response_model=ReportResponse,
)
def get_report(
    report_id: UUID,
    service: Annotated[
        ReportService,
        Depends(get_report_service),
    ],
):
    report = service.get_report(report_id)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found.",
        )

    return APIReportMapper.from_domain(report)