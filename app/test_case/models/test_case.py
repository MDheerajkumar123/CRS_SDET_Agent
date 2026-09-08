from enum import Enum

from pydantic import BaseModel, Field


class TestCaseType(str, Enum):
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


class TestCase(BaseModel):
    test_case_id: str
    design_id: str
    scenario_id: str
    requirement_id: str

    title: str
    objective: str
    test_type: TestCaseType
    priority: str

    preconditions: list[str] = Field(default_factory=list)
    test_data: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    expected_results: list[str] = Field(default_factory=list)

    source_design: str


class TestCaseAnalysis(BaseModel):
    document_name: str
    test_case_summary: str

    test_cases: list[TestCase] = Field(default_factory=list)

    overall_test_case_confidence: float = Field(..., ge=0, le=1)
