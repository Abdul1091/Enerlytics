"""Tests for ConfidenceScore."""

import pytest

from app.domain.reporting.exceptions import InvalidConfidenceScoreError
from app.domain.reporting.value_objects import ConfidenceScore


def test_accepts_zero():
    score = ConfidenceScore(0.0)
    assert score.value == 0.0


def test_accepts_one():
    score = ConfidenceScore(1.0)
    assert score.value == 1.0


def test_accepts_middle_value():
    score = ConfidenceScore(0.57)
    assert score.value == 0.57


@pytest.mark.parametrize(
    "value",
    [-0.1, -1.0, 1.1, 2.0],
)
def test_rejects_invalid_scores(value):
    with pytest.raises(InvalidConfidenceScoreError):
        ConfidenceScore(value)