"""Exceptions for the Reporting domain."""


class ReportingError(Exception):
    """Base exception for all reporting domain errors."""


class InvalidConfidenceScoreError(ReportingError):
    """Raised when a confidence score is outside the allowed range."""


class InvalidGeoLocationError(ReportingError):
    """Raised when a geographic location is invalid."""


class InvalidObservationTimeError(ReportingError):
    """Raised when an observation time violates business rules."""


class InvalidReportStatusTransitionError(ReportingError):
    """Raised when an invalid report status transition is attempted."""


class InvalidEvidenceError(ReportingError):
    """Raised when report evidence is invalid."""