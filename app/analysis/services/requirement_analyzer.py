from app.analysis.prompts.crs_analyzer import (
    build_crs_analyzer_prompt,
)
from app.analysis.retrieval.retriever import CRSRetriever
from app.analysis.parsers.requirement_parser import (
    RequirementAnalysisParser,
)
from app.llm.manager import LLMManager


class RequirementAnalyzer:
    """
    Coordinates CRS retrieval, prompt construction, LLM generation,
    and structured requirement validation.
    """

    def __init__(
        self,
        retriever=None,
        llm_manager=None,
    ):
        self.retriever = retriever or CRSRetriever()
        self.llm_manager = llm_manager or LLMManager()

    def analyze(
        self,
        document_name: str,
        query: str,
        n_results: int = 5,
    ):
        if not document_name or not document_name.strip():
            raise ValueError("Document name is required.")

        if not query or not query.strip():
            raise ValueError("Analysis query is required.")

        # 1. Retrieve relevant CRS context
        retrieved_results = self.retriever.search(
            query=query,
            n_results=n_results,
        )

        if not retrieved_results:
            raise ValueError(
                "No relevant CRS context was retrieved."
            )

        # 2. Build traceable context for the LLM
        context_parts = []

        for result in retrieved_results:
            context_parts.append(
                f"[{result.section_id} | {result.section_title}]\n"
                f"{result.content}"
            )

        retrieved_context = "\n\n".join(context_parts)

        # 3. Build analyzer prompt
        prompt = build_crs_analyzer_prompt(
            document_name=document_name,
            retrieved_context=retrieved_context,
        )

        # 4. Generate using the configured LLM
        llm_response = self.llm_manager.generate(
            task_name="crs_analyzer",
            prompt=prompt,
        )

        # 5. Validate and convert LLM output
        analysis = RequirementAnalysisParser.parse(
            llm_response.content
        )

        return analysis, llm_response
