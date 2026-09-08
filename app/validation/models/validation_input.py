from pydantic import BaseModel, Field

from app.analysis.models.requirement import RequirementAnalysis


class ValidationInput(BaseModel):
    analysis: RequirementAnalysis
    validation_focus: str = Field(
        default=(
            "Validate completeness, classification, hallucination, "
            "source traceability, duplicates, business-rule traceability, "
            "dependencies, testability, ambiguity, and confidence."
        )
    )
