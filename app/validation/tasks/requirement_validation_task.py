from crewai import Task

from app.validation.agents.requirement_validation_agent import (
    RequirementValidationAgent,
)
from app.validation.models.review_result import ReviewResult


def create_requirement_validation_task(
    analysis_json: str,
) -> Task:

    reviewer = RequirementValidationAgent().get_agent()

    return Task(
        description=(
            "Review the supplied RequirementAnalysis produced by the "
            "CRS Analyzer Agent.\n\n"
            "Validate requirement completeness, classification, "
            "hallucination or unsupported inference, source "
            "traceability, duplicates, business-rule traceability, "
            "dependency validity, testability, missing or ambiguous "
            "requirements, and confidence scores.\n\n"
            "Do not rewrite or silently modify requirements. "
            "Identify material issues and provide actionable "
            "required changes when rework is necessary.\n\n"
            f"RequirementAnalysis to review:\n{analysis_json}"
        ),
        expected_output=(
            "A structured ReviewResult containing PASS or REWORK "
            "status, a quality score from 0 to 100, identified "
            "issues, and required changes."
        ),
        agent=reviewer,
        output_pydantic=ReviewResult,
    )
