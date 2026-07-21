"""Tests for ObservationTime."""

from datetime import UTC, datetime, timedelta

import pytest

from app.domain.reporting.exceptions import InvalidObservationTimeError
from app.domain.reporting.value_objects import ObservationTime


def test_accepts_past_time():
    value = datetime.now(UTC) - timedelta(hours=2)

    observation = ObservationTime(value)

    assert observation.value == value


def test_rejects_future_time():
    future = datetime.now(UTC) + timedelta(hours=1)

    with pytest.raises(InvalidObservationTimeError):
        ObservationTime(future)