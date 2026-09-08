
import json

from app.final_review.models.review_result import FinalQAReviewResult
from app.final_review.prompts.final_qa_reviewer import (
    build_final_qa_reviewer_prompt,
)
from app.llm.manager import LLMManager


class FinalQAReviewerService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def review(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_context: str,
        rtm_context: str,
    ) -> FinalQAReviewResult:
        prompt = build_final_qa_reviewer_prompt(
            document_name=document_name,
            requirement_context=requirement_context,
            risk_strategy_context=risk_strategy_context,
            scenario_context=scenario_context,
            test_design_context=test_design_context,
            test_case_context=test_case_context,
            rtm_context=rtm_context,
        )

        response = self.llm_manager.generate(
            task_name="final_reviewer",
            prompt=prompt,
        )

        content = response.content.strip()

        if content.startswith("```"):
            lines = content.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            content = "\n".join(lines).strip()

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Final QA reviewer returned invalid JSON."
            ) from exc

        return FinalQAReviewResult.model_validate(data)
