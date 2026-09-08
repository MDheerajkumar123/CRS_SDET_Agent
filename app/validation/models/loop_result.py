from app.analysis.models.requirement import RequirementAnalysis
from app.validation.models.review_result import ReviewResult
from pydantic import BaseModel, Field


class ValidationLoopResult(BaseModel):
    final_analysis: RequirementAnalysis
    final_review: ReviewResult
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=1)
    passed: bool
