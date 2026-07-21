"""Shared pytest fixtures."""

from datetime import UTC, datetime, timedelta

import pytest

from app.domain.reporting.enums import ReportType
from app.domain.reporting.report import Report
from app.domain.reporting.value_objects import (
    GeoLocation,
    ObservationTime,
)


@pytest.fixture
def valid_location() -> GeoLocation:
    return GeoLocation(
        latitude=9.0820,
        longitude=8.6753,
    )


@pytest.fixture
def valid_observation_time() -> ObservationTime:
    return ObservationTime(
        datetime.now(UTC) - timedelta(minutes=10)
    )


@pytest.fixture
def report(
    valid_location: GeoLocation,
    valid_observation_time: ObservationTime,
) -> Report:
    return Report(
        report_type=ReportType.POWER_OUTAGE,
        location=valid_location,
        observed_at=valid_observation_time,
        description="No electricity since yesterday.",
    )