from pydantic import BaseModel, Field

from app.validation.models.review_result import ReviewResult


class ReworkRequest(BaseModel):
    review: ReviewResult
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=1)
