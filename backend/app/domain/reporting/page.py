from __future__ import annotations

from dataclasses import dataclass

from .report import Report


@dataclass(slots=True)
class ReportPage:
    items: list[Report]
    total: int
    limit: int
    offset: int