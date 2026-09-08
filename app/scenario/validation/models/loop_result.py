from pydantic import BaseModel, Field

from app.scenario.models.test_scenario import ScenarioAnalysis
from app.scenario.validation.models.review_result import (
    ScenarioReviewResult,
)


class ScenarioValidationLoopResult(BaseModel):
    final_scenarios: ScenarioAnalysis
    final_review: ScenarioReviewResult
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=1)
    passed: bool
