
from pydantic import BaseModel, Field


class FinalQAReworkRequest(BaseModel):
    document_name: str

    requirement_context: str
    risk_strategy_context: str
    scenario_context: str
    test_design_context: str
    test_case_context: str
    rtm_context: str

    issues: list[str] = Field(default_factory=list)
    required_changes: list[str] = Field(default_factory=list)

    retry_count: int = Field(default=0, ge=0)
