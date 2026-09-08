
import json

from app.llm.manager import LLMManager
from app.rtm.models.rtm import RTMAnalysis
from app.rtm.validation.models.review_result import RTMReviewResult
from app.rtm.validation.prompts.rtm_validator import (
    build_rtm_validator_prompt,
)


class RTMValidatorService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def validate(
        self,
        document_name: str,
        requirement_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_context: str,
        rtm_analysis: RTMAnalysis,
    ) -> RTMReviewResult:
        if not isinstance(rtm_analysis, RTMAnalysis):
            raise TypeError("rtm_analysis must be an RTMAnalysis instance.")

        rtm_context = json.dumps(
            rtm_analysis.model_dump(),
            indent=2,
        )

        prompt = build_rtm_validator_prompt(
            document_name=document_name,
            requirement_context=requirement_context,
            scenario_context=scenario_context,
            test_design_context=test_design_context,
            test_case_context=test_case_context,
            rtm_context=rtm_context,
        )

        response = self.llm_manager.generate(
            task_name="rtm_validator",
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
                "RTM validator returned invalid JSON."
            ) from exc

        return RTMReviewResult.model_validate(data)
