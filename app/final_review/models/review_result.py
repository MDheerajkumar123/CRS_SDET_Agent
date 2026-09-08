
from enum import Enum

from pydantic import BaseModel, Field


class FinalReviewStatus(str, Enum):
    PASS = "PASS"
    REWORK = "REWORK"


class FinalQAReviewResult(BaseModel):
    status: FinalReviewStatus
    score: int = Field(..., ge=0, le=100)
    issues: list[str] = Field(default_factory=list)
    required_changes: list[str] = Field(default_factory=list)
    review_summary: str = ""
