import json

from app.analysis.models.requirement import RequirementAnalysis
from app.llm.manager import LLMManager
from app.strategy.models.test_strategy import TestStrategy
from app.strategy.prompts.test_strategy import build_test_strategy_prompt


class TestStrategyService:
    def __init__(self, llm_manager: LLMManager):
        self.llm_manager = llm_manager

    def generate_strategy(
        self,
        analysis: RequirementAnalysis,
    ) -> TestStrategy:
        requirement_context = self._build_requirement_context(analysis)

        prompt = build_test_strategy_prompt(
            document_name=analysis.document_name,
            requirement_context=requirement_context,
        )

        llm_response = self.llm_manager.generate(
            task_name="risk_strategy",
            prompt=prompt,
        )

        raw_response = self._extract_response_content(llm_response)

        return self._parse_strategy_response(raw_response)

    @staticmethod
    def _build_requirement_context(
        analysis: RequirementAnalysis,
    ) -> str:
        lines = []

        for requirement in analysis.requirements:
            lines.append(
                "\n".join(
                    [
                        f"Requirement ID: {requirement.requirement_id}",
                        f"Title: {requirement.title}",
                        f"Description: {requirement.description}",
                        f"Type: {requirement.requirement_type.value}",
                        f"Classification: {requirement.classification.value}",
                        f"Business Rules: {requirement.business_rules}",
                        f"Dependencies: {requirement.dependencies}",
                        f"Source Section: {requirement.source_section}",
                    ]
                )
            )

        return "\n\n--- REQUIREMENT ---\n\n".join(lines)

    @staticmethod
    def _extract_response_content(llm_response) -> str:
        if hasattr(llm_response, "content"):
            content = llm_response.content
        else:
            content = str(llm_response)

        if not content or not content.strip():
            raise ValueError(
                "Risk & Test Strategy LLM response is empty."
            )

        return content.strip()

    @staticmethod
    def _parse_strategy_response(
        raw_response: str,
    ) -> TestStrategy:
        cleaned_response = raw_response.strip()

        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

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
                        f"Risk & Test Strategy response is not valid JSON: {exc}"
                    ) from exc
            else:
                raise ValueError(
                    f"Risk & Test Strategy response is not valid JSON: {exc}"
                ) from exc

        try:
            return TestStrategy.model_validate(data)
        except Exception as exc:
            raise ValueError(
                "Risk & Test Strategy response does not conform "
                f"to TestStrategy schema: {exc}"
            ) from exc
