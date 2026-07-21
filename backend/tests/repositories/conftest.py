"""Fixtures for repository tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta



import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.domain.reporting.enums import ReportType
from app.domain.reporting.report import Report
from app.domain.reporting.value_objects import (
    GeoLocation,
    ObservationTime,
)
from app.infrastructure.persistence.sqlalchemy_report_repository import (
    SQLAlchemyReportRepository,
)
from app.core.config import TestSettings

settings = TestSettings()

engine = create_engine(settings.DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
def create_database():
    """
    Create the schema once for the entire test session.
    """
    Base.metadata.create_all(engine)

    yield

    Base.metadata.drop_all(engine)


@pytest.fixture
def connection():
    """
    Provide a database connection wrapped in a transaction.

    Every test is rolled back to keep the database clean.
    """
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture
def session(connection):
    """
    SQLAlchemy session used by repository tests.
    """
    session = Session(bind=connection)

    yield session

    session.close()


@pytest.fixture
def repository(session):
    """
    SQLAlchemy implementation of the ReportRepository.
    """
    return SQLAlchemyReportRepository(session)


@pytest.fixture
def report():
    """
    Sample report entity.
    """
    return Report(
        report_type=ReportType.POWER_OUTAGE,
        location=GeoLocation(
            latitude=9.0820,
            longitude=8.6753,
        ),
        observed_at=ObservationTime(
            datetime.now(UTC) - timedelta(minutes=15)
        ),
        description="Power outage affecting the community.",
    )