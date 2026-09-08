from enum import Enum

from pydantic import BaseModel, Field


class ReworkArtifact(str, Enum):
    REQUIREMENTS = "REQUIREMENTS"
    RISK_STRATEGY = "RISK_STRATEGY"
    SCENARIOS = "SCENARIOS"
    TEST_DESIGNS = "TEST_DESIGNS"
    TEST_CASES = "TEST_CASES"
    RTM = "RTM"


class ReworkTarget(BaseModel):
    artifact: ReworkArtifact
    reason: str
    actions: list[str] = Field(default_factory=list)


class ReworkRoutingResult(BaseModel):
    document_name: str
    targets: list[ReworkTarget] = Field(default_factory=list)
    routing_summary: str
