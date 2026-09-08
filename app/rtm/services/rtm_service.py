
import json

from app.llm.manager import LLMManager
from app.rtm.models.rtm import RTMAnalysis
from app.rtm.prompts.rtm import build_rtm_prompt


class RTMService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def generate(
        self,
        document_name: str,
        requirement_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_context: str,
    ) -> RTMAnalysis:
        prompt = build_rtm_prompt(
            document_name=document_name,
            requirement_context=requirement_context,
            scenario_context=scenario_context,
            test_design_context=test_design_context,
            test_case_context=test_case_context,
        )

        response = self.llm_manager.generate(
            task_name="rtm",
            prompt=prompt,
        )

        return self._parse_response(response.content)

    @staticmethod
    def _parse_response(content: str) -> RTMAnalysis:
        if not content or not content.strip():
            raise ValueError("RTM LLM response is empty.")

        cleaned = content.strip()

        if cleaned.startswith("```"):
            lines = cleaned.splitlines()

            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned = "\n".join(lines).strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"RTM LLM response is not valid JSON: {exc}"
            ) from exc

        try:
            return RTMAnalysis.model_validate(data)
        except Exception as exc:
            raise ValueError(
                f"RTM LLM response failed RTMAnalysis validation: {exc}"
            ) from exc
