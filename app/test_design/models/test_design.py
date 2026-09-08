from enum import Enum

from pydantic import BaseModel, Field


class TestDesignTechnique(str, Enum):
    EQUIVALENCE_PARTITIONING = "Equivalence Partitioning"
    BOUNDARY_VALUE_ANALYSIS = "Boundary Value Analysis"
    DECISION_TABLE = "Decision Table"
    STATE_TRANSITION = "State Transition"
    ERROR_GUESSING = "Error Guessing"
    PAIRWISE = "Pairwise"
    USE_CASE = "Use Case"


class TestDesign(BaseModel):
    design_id: str
    scenario_id: str
    requirement_id: str

    title: str
    objective: str

    test_design_technique: TestDesignTechnique

    test_data_conditions: list[str] = Field(default_factory=list)

    coverage_area: str

    expected_focus: str

    source_scenario: str


class TestDesignAnalysis(BaseModel):
    document_name: str
    design_summary: str

    test_designs: list[TestDesign] = Field(default_factory=list)

    overall_design_confidence: float = Field(..., ge=0, le=1)
