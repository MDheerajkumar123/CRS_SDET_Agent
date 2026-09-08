
from pydantic import BaseModel, Field

from app.final_review.models.review_result import FinalQAReviewResult
from app.final_review.models.rework_request import FinalQAReworkRequest


class FinalQAValidationLoopResult(BaseModel):
    final_review: FinalQAReviewResult
    final_rework_request: FinalQAReworkRequest | None = None
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=0)
    passed: bool
