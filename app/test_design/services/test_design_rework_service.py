
import json

from app.llm.manager import LLMManager
from app.test_design.models.test_design import (
    TestDesignAnalysis,
)
from app.test_design.prompts.test_design_rework import (
    build_test_design_rework_prompt,
)


class TestDesignReworkService:
    __test__ = False
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def rework(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        scenario_context: str,
        current_design_context: str,
        issues: list[str],
        required_changes: list[str],
        retry_count: int = 0,
    ) -> TestDesignAnalysis:

        prompt = build_test_design_rework_prompt(
            document_name=document_name,
            requirement_context=requirement_context,
            risk_strategy_context=risk_strategy_context,
            scenario_context=scenario_context,
            current_design_context=current_design_context,
            issues=issues,
            required_changes=required_changes,
            retry_count=retry_count,
        )

        llm_response = self.llm_manager.generate(
            task_name="test_design",
            prompt=prompt,
        )

        content = (
            llm_response.content
            if hasattr(llm_response, "content")
            else str(llm_response)
        )

        if not content or not content.strip():
            raise ValueError(
                "Test Design rework LLM response is empty."
            )

        cleaned_response = content.strip()

        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()

            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

        try:
            data = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            start = cleaned_response.find("{")
            end = cleaned_response.rfind("}")

            if start != -1 and end != -1:
                candidate = cleaned_response[start:end + 1]

                try:
                    data = json.loads(candidate)
                except json.JSONDecodeError:
                    raise ValueError(
                        "Test Design rework response is not valid JSON."
                    ) from exc
            else:
                raise ValueError(
                    "Test Design rework response is not valid JSON."
                ) from exc

        try:
            return TestDesignAnalysis.model_validate(data)
        except Exception as exc:
            raise ValueError(
                "Test Design rework response does not conform "
                f"to TestDesignAnalysis schema: {exc}"
            ) from exc
