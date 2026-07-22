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
from app.api.schemas.report_query import (
    ReportPageResponse,
    ReportQueryParams,
)

from app.api.dependencies import (
    get_report_analyzer,
    get_report_service,
)

from app.api.schemas.report_analysis import (
    ReportAnalysisResponse,
)

from app.infrastructure.ai.analyzer import (
    ReportAnalyzer,
)

from app.api.mappers import (
    APIReportMapper,
    ReportAnalysisMapper,
    ReportQueryMapper,
)

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


@router.get(
    "",
    response_model=ReportPageResponse,
)
def list_reports(
    params: Annotated[
        ReportQueryParams,
        Depends(),
    ],
    service: Annotated[
        ReportService,
        Depends(get_report_service),
    ],
):
    query = ReportQueryMapper.to_domain(params)

    page = service.list_reports(query)

    return ReportPageResponse(
        items=[
            APIReportMapper.from_domain(report)
            for report in page.items
        ],
        total=page.total,
        limit=page.limit,
        offset=page.offset,
    )


@router.get(
    "/{report_id}/analysis",
    response_model=ReportAnalysisResponse,
)
def analyze_report(
    report_id: UUID,
    service: Annotated[
        ReportService,
        Depends(get_report_service),
    ],
    analyzer: Annotated[
        ReportAnalyzer,
        Depends(get_report_analyzer),
    ],
):
    """
    Generate an AI analysis for a report.
    """
    report = service.get_report(report_id)

    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found.",
        )

    analysis = analyzer.analyze(report)

    return ReportAnalysisMapper.from_domain(
        analysis
    )