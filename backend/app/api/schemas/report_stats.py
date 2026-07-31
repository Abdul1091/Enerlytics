"""Pydantic schemas for Report Analytics & Statistics."""

from __future__ import annotations

from typing import Dict, List
from pydantic import BaseModel, Field


class ReportStatsResponse(BaseModel):
    total_reports: int
    pending_count: int
    resolved_count: int
    verified_count: int
    rejected_count: int
    avg_confidence_score: float
    type_distribution: Dict[str, int] = Field(default_factory=dict)
    severity_distribution: Dict[str, int] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class TrendItem(BaseModel):
    date: str
    total: int
    critical: int


class ReportTrendsResponse(BaseModel):
    trends: List[TrendItem]

    class Config:
        from_attributes = True