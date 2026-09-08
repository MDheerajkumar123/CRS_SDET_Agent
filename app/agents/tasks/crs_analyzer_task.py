from crewai import Task

from app.agents.crs_analyzer_agent import (
    CRSAnalyzerAgent,
)
from app.analysis.models.requirement import RequirementAnalysis


def create_crs_analyzer_task(
    document_name: str,
    query: str,
    n_results: int = 5,
) -> Task:
    """
    Create the CrewAI task responsible for CRS requirement analysis.
    """

    analyzer_agent = CRSAnalyzerAgent().get_agent()

    return Task(
        description=(
            f"Analyze the CRS document '{document_name}' "
            f"for the following analysis focus:\n\n"
            f"{query}\n\n"
            f"Retrieve the relevant CRS evidence using the available "
            f"CRS Requirement Analyzer tool. Extract only requirements "
            f"supported by the CRS evidence. Preserve source "
            f"traceability and do not invent missing requirements."
        ),
        expected_output=(
            "A validated requirement analysis containing the CRS "
            "document name, analysis summary, requirements, source "
            "traceability, business rules, dependencies, and "
            "confidence scores."
        ),
        agent=analyzer_agent,
        output_pydantic=RequirementAnalysis,
    )
