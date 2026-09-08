
from pydantic import BaseModel, Field

from app.rtm.models.rtm import RTMAnalysis
from app.rtm.validation.models.review_result import RTMReviewResult


class RTMValidationLoopResult(BaseModel):
    final_rtm: RTMAnalysis
    final_review: RTMReviewResult
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=0)
    passed: bool
