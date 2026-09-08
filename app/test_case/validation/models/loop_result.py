from pydantic import BaseModel, Field

from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.models.review_result import TestCaseReviewResult


class TestCaseValidationLoopResult(BaseModel):
    final_test_cases: TestCaseAnalysis
    final_review: TestCaseReviewResult
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=0)
    passed: bool
