"""Value objects for the Reporting domain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from .exceptions import (
    InvalidConfidenceScoreError,
    InvalidGeoLocationError,
    InvalidObservationTimeError,
)


@dataclass(frozen=True, slots=True)
class ConfidenceScore:
    """
    Represents the confidence assigned to a report.

    The value must always be between 0.0 and 1.0.
    """

    value: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 1.0:
            raise InvalidConfidenceScoreError(
                "Confidence score must be between 0.0 and 1.0."
            )


@dataclass(frozen=True, slots=True)
class GeoLocation:
    """
    Represents the geographic location where an event occurred.
    """

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90 <= self.latitude <= 90:
            raise InvalidGeoLocationError(
                "Latitude must be between -90 and 90 degrees."
            )

        if not -180 <= self.longitude <= 180:
            raise InvalidGeoLocationError(
                "Longitude must be between -180 and 180 degrees."
            )


@dataclass(frozen=True, slots=True)
class ObservationTime:
    """
    Represents the time an electricity event was observed.
    """

    value: datetime

    def __post_init__(self) -> None:
        if self.value.tzinfo is None:
            raise InvalidObservationTimeError(
                "Observation time must be timezone-aware."
            )

        if self.value > datetime.now(UTC):
            raise InvalidObservationTimeError(
                "Observation time cannot be in the future."
            )