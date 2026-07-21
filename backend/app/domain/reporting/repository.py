"""Repository contract for the Reporting domain."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from .report import Report


class ReportRepository(ABC):
    """
    Defines how reports are stored and retrieved.

    The domain depends on this abstraction rather than
    any specific database technology.
    """

    @abstractmethod
    def save(self, report: Report) -> Report:
        """Persist a report."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, report_id: UUID) -> Report | None:
        """Retrieve a report by its identifier."""
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Report]:
        """Return all reports."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, report_id: UUID) -> None:
        """Delete a report."""
        raise NotImplementedError