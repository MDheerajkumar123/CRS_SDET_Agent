
from app.llm.manager import LLMManager
from app.strategy.models.test_strategy import TestStrategy
from app.strategy.prompts.risk_strategy_rework import (
    build_risk_strategy_rework_prompt,
)


class RiskStrategyReworkService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def rework(
        self,
        document_name: str,
        requirement_context: str,
        current_strategy: str,
        issues: list[str],
        required_changes: list[str],
        retry_count: int = 0,
    ) -> TestStrategy:

        prompt = build_risk_strategy_rework_prompt(
            document_name=document_name,
            requirement_context=requirement_context,
            current_strategy=current_strategy,
            issues=issues,
            required_changes=required_changes,
            retry_count=retry_count,
        )

        llm_response = self.llm_manager.generate(
            task_name="risk_strategy",
            prompt=prompt,
        )

        content = (
            llm_response.content
            if hasattr(llm_response, "content")
            else str(llm_response)
        )

        if not content or not content.strip():
            raise ValueError(
                "Risk Strategy rework LLM response is empty."
            )

        cleaned_response = content.strip()

        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

        import json

        try:
            data = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            start = cleaned_response.find("{")
            end = cleaned_response.rfind("}")

            if start != -1 and end != -1 and end > start:
                candidate = cleaned_response[start:end + 1]

                try:
                    data = json.loads(candidate)
                except json.JSONDecodeError:
                    raise ValueError(
                        "Risk Strategy rework response is not valid JSON."
                    ) from exc
            else:
                raise ValueError(
                    "Risk Strategy rework response is not valid JSON."
                ) from exc

        try:
            return TestStrategy.model_validate(data)
        except Exception as exc:
            raise ValueError(
                "Risk Strategy rework response does not conform "
                f"to TestStrategy schema: {exc}"
            ) from exc
