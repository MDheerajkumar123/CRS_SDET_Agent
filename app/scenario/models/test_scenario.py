from enum import Enum

from pydantic import BaseModel, Field


class ScenarioType(str, Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    BOUNDARY = "Boundary"
    ERROR = "Error"
    INTEGRATION = "Integration"
    SECURITY = "Security"
    PERFORMANCE = "Performance"
    RELIABILITY = "Reliability"
    USABILITY = "Usability"
    COMPATIBILITY = "Compatibility"
    REGRESSION = "Regression"


class TestScenario(BaseModel):
    scenario_id: str
    requirement_id: str
    title: str
    description: str
    scenario_type: ScenarioType
    priority: str
    preconditions: list[str] = Field(default_factory=list)
    expected_behavior: str
    source_requirement: str


class ScenarioAnalysis(BaseModel):
    document_name: str
    scenario_summary: str
    scenarios: list[TestScenario] = Field(default_factory=list)
    overall_scenario_confidence: float = Field(..., ge=0, le=1)
