
from enum import Enum

from pydantic import BaseModel, Field


class CoverageStatus(str, Enum):
    COVERED = "Covered"
    PARTIAL = "Partial"
    NOT_COVERED = "Not Covered"


class RequirementCoverage(BaseModel):
    requirement_id: str
    scenario_ids: list[str] = Field(default_factory=list)
    design_ids: list[str] = Field(default_factory=list)
    test_case_ids: list[str] = Field(default_factory=list)
    coverage_status: CoverageStatus
    coverage_notes: str = ""


class RTMAnalysis(BaseModel):
    document_name: str
    rtm_summary: str
    requirement_coverage: list[RequirementCoverage] = Field(
        default_factory=list
    )
    total_requirements: int = Field(default=0, ge=0)
    covered_requirements: int = Field(default=0, ge=0)
    partially_covered_requirements: int = Field(default=0, ge=0)
    not_covered_requirements: int = Field(default=0, ge=0)
    overall_coverage_percentage: float = Field(
        default=0.0,
        ge=0,
        le=100,
    )
