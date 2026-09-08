from app.analysis.models.requirement import RequirementAnalysis
from app.analysis.parsers.requirement_parser import (
    RequirementAnalysisParser,
)
from app.llm.manager import LLMManager
from app.validation.models.review_result import ReviewResult
from app.validation.prompts.rework_prompt import build_rework_prompt


class RequirementReworkService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def rework(
        self,
        analysis: RequirementAnalysis,
        review: ReviewResult,
    ) -> tuple[RequirementAnalysis, object]:

        if not isinstance(analysis, RequirementAnalysis):
            raise TypeError(
                "analysis must be a RequirementAnalysis instance."
            )

        if not isinstance(review, ReviewResult):
            raise TypeError(
                "review must be a ReviewResult instance."
            )

        if review.status.value != "REWORK":
            raise ValueError(
                "Rework can only be performed when review status is REWORK."
            )

        prompt = build_rework_prompt(
            analysis=analysis,
            review=review,
        )

        llm_response = self.llm_manager.generate(
            task_name="crs_analyzer",
            prompt=prompt,
        )

        revised_analysis = RequirementAnalysisParser.parse(
            llm_response.content
        )

        return revised_analysis, llm_response
