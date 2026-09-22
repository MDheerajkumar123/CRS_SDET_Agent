from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from app.analysis.retrieval.retriever import CRSRetriever


class CRSAnalyzerToolInput(BaseModel):
    document_name: str = Field(
        ...,
        description="Name of the CRS document being analyzed.",
    )

    query: str = Field(
        ...,
        description=(
            "Question or analysis focus used to retrieve relevant "
            "CRS requirements."
        ),
    )

    n_results: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of relevant CRS chunks to retrieve.",
    )


class CRSAnalyzerTool(BaseTool):
    name: str = "CRS Requirement Analyzer"

    description: str = (
        "Retrieve relevant evidence from the supplied CRS document. "
        "Use the returned evidence to analyze requirements. "
        "Do not invent information that is not present in the evidence."
    )

    args_schema: type[BaseModel] = CRSAnalyzerToolInput

    def _run(
        self,
        document_name: str,
        query: str,
        n_results: int = 5,
    ) -> str:

        retriever = CRSRetriever()

        retrieved_results = retriever.search(
            query=query,
            n_results=n_results,
            document_name=document_name,
        )

        if not retrieved_results:
            return (
                f"No relevant CRS evidence found for "
                f"document '{document_name}'."
            )

        evidence_parts = []

        for result in retrieved_results:
            page = (
                str(result.page_number)
                if result.page_number is not None
                else "N/A"
            )

            evidence_parts.append(
                f"[Document: {result.source_document}]\n"
                f"[Section: {result.section_id} | "
                f"{result.section_title}]\n"
                f"[Page: {page}]\n"
                f"[Distance: {result.distance:.4f}]\n"
                f"Evidence:\n{result.content}"
            )

        return "\n\n".join(evidence_parts)
