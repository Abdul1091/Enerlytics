"""Enumerations for the Reporting domain."""

from enum import StrEnum


class ReportType(StrEnum):
    """Types of electricity-related reports supported by Enerlytics."""

    POWER_OUTAGE = "power_outage"
    LOW_VOLTAGE = "low_voltage"
    HIGH_VOLTAGE = "high_voltage"
    TRANSFORMER_FAULT = "transformer_fault"
    FALLEN_CABLE = "fallen_cable"
    METER_ISSUE = "meter_issue"
    STREETLIGHT_FAULT = "streetlight_fault"
    OTHER = "other"


class ReportStatus(StrEnum):
    """Lifecycle states of a report."""

    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    VALIDATED = "validated"
    REJECTED = "rejected"
    RESOLVED = "resolved"


class EvidenceType(StrEnum):
    """Supported evidence types."""

    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    NOTE = "note"