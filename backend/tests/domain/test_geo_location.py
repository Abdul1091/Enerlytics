"""Tests for GeoLocation."""

import pytest

from app.domain.reporting.exceptions import InvalidGeoLocationError
from app.domain.reporting.value_objects import GeoLocation


def test_accepts_valid_coordinates():
    location = GeoLocation(
        latitude=9.0820,
        longitude=8.6753,
    )

    assert location.latitude == 9.0820
    assert location.longitude == 8.6753


@pytest.mark.parametrize(
    "latitude",
    [-91.0, 91.0],
)
def test_invalid_latitude(latitude):
    with pytest.raises(InvalidGeoLocationError):
        GeoLocation(
            latitude=latitude,
            longitude=8.0,
        )


@pytest.mark.parametrize(
    "longitude",
    [-181.0, 181.0],
)
def test_invalid_longitude(longitude):
    with pytest.raises(InvalidGeoLocationError):
        GeoLocation(
            latitude=8.0,
            longitude=longitude,
        )