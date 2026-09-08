from enum import Enum

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TestType(str, Enum):
    FUNCTIONAL = "Functional"
    NEGATIVE = "Negative"
    BOUNDARY = "Boundary"
    INTEGRATION = "Integration"
    REGRESSION = "Regression"
    SECURITY = "Security"
    PERFORMANCE = "Performance"
    USABILITY = "Usability"
    COMPATIBILITY = "Compatibility"
    RELIABILITY = "Reliability"
    AUDITABILITY = "Auditability"


class RequirementRisk(BaseModel):
    requirement_id: str
    risk_level: RiskLevel
    risk_score: int = Field(..., ge=1, le=100)
    risk_reason: str
    impacted_areas: list[str] = Field(default_factory=list)
    recommended_test_types: list[TestType] = Field(default_factory=list)


class TestStrategy(BaseModel):
    document_name: str
    strategy_summary: str
    requirement_risks: list[RequirementRisk] = Field(default_factory=list)
    prioritized_requirements: list[str] = Field(default_factory=list)
    overall_risk_level: RiskLevel
    overall_strategy_confidence: float = Field(..., ge=0, le=1)
