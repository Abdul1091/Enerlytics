"""Tests for the Reports API."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from app.db.models.report import ReportModel
from app.db.session import SessionLocal
from app.domain.reporting.enums import (
    ReportStatus,
    ReportType,
)


@pytest.fixture(autouse=True)
def clear_database():
    """
    Ensure every API test starts with an empty reports table.
    """
    session = SessionLocal()

    session.query(ReportModel).delete()
    session.commit()
    session.close()


def create_report(client, **overrides):
    payload = {
        "report_type": ReportType.POWER_OUTAGE.value,
        "latitude": 11.85,
        "longitude": 13.15,
        "description": "No electricity.",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "reporter_id": str(uuid4()),
    }

    payload.update(overrides)

    response = client.post("/reports", json=payload)
    print(response.json())

    assert response.status_code == 201, response.text

    return response.json()


def test_create_report(client):
    report = create_report(client)

    assert report["report_type"] == ReportType.POWER_OUTAGE.value
    assert report["status"] == ReportStatus.SUBMITTED.value


def test_get_existing_report(client):
    created = create_report(client)

    response = client.get(f"/reports/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_unknown_report(client):
    response = client.get(f"/reports/{uuid4()}")

    assert response.status_code == 404


def test_list_reports_returns_items(client):
    create_report(client)
    create_report(client)

    response = client.get("/reports")

    assert response.status_code == 200

    page = response.json()

    assert page["total"] == 2
    assert len(page["items"]) == 2


def test_pagination(client):
    for _ in range(5):
        create_report(client)

    response = client.get(
        "/reports",
        params={
            "limit": 2,
            "offset": 1,
        },
    )

    assert response.status_code == 200

    page = response.json()

    assert page["limit"] == 2
    assert page["offset"] == 1
    assert len(page["items"]) == 2


def test_filter_by_report_type(client):
    create_report(
        client,
        report_type=ReportType.POWER_OUTAGE.value,
    )

    create_report(
        client,
        report_type=ReportType.LOW_VOLTAGE.value,
    )

    response = client.get(
        "/reports",
        params={
            "report_type": ReportType.LOW_VOLTAGE.value,
        },
    )

    page = response.json()

    assert page["total"] == 1
    assert page["items"][0]["report_type"] == ReportType.LOW_VOLTAGE.value


def test_filter_by_reporter(client):
    reporter = uuid4()

    create_report(
        client,
        reporter_id=str(reporter),
    )

    create_report(
        client,
        reporter_id=str(uuid4()),
    )

    response = client.get(
        "/reports",
        params={
            "reporter_id": str(reporter),
        },
    )

    page = response.json()

    assert page["total"] == 1
    assert page["items"][0]["reporter_id"] == str(reporter)


def test_filter_by_date_range(client):
    old_time = (
        datetime.now(timezone.utc)
        - timedelta(days=5)
    )

    new_time = datetime.now(timezone.utc)

    create_report(
        client,
        observed_at=old_time.isoformat(),
    )

    create_report(
        client,
        observed_at=new_time.isoformat(),
    )

    response = client.get(
        "/reports",
        params={
            "observed_from": (
                datetime.now(timezone.utc)
                - timedelta(days=1)
            ).isoformat()
        },
    )

    page = response.json()

    assert page["total"] == 1


def test_sort_descending(client):
    create_report(
        client,
        observed_at=(
            datetime.now(timezone.utc)
            - timedelta(days=2)
        ).isoformat(),
    )

    newest = create_report(
        client,
        observed_at=datetime.now(
            timezone.utc
        ).isoformat(),
    )

    response = client.get(
        "/reports",
        params={
            "sort_by": "observed_at",
            "descending": True,
        },
    )

    page = response.json()

    assert page["items"][0]["id"] == newest["id"]


def test_sort_ascending(client):
    oldest = create_report(
        client,
        observed_at=(
            datetime.now(timezone.utc)
            - timedelta(days=2)
        ).isoformat(),
    )

    create_report(
        client,
        observed_at=datetime.now(
            timezone.utc
        ).isoformat(),
    )

    response = client.get(
        "/reports",
        params={
            "sort_by": "observed_at",
            "descending": False,
        },
    )

    page = response.json()

    assert page["items"][0]["id"] == oldest["id"]