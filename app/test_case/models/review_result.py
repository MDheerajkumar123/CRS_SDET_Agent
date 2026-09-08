from enum import Enum

from pydantic import BaseModel, Field


class TestCaseReviewStatus(str, Enum):
    PASS = "PASS"
    REWORK = "REWORK"


class TestCaseReviewResult(BaseModel):
    status: TestCaseReviewStatus
    score: int = Field(..., ge=0, le=100)
    issues: list[str] = Field(default_factory=list)
    required_changes: list[str] = Field(default_factory=list)
