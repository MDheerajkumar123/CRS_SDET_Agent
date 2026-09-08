import json

from app.analysis.models.requirement import RequirementAnalysis
from app.llm.manager import LLMManager
from app.scenario.models.test_scenario import ScenarioAnalysis
from app.scenario.prompts.test_scenario import build_test_scenario_prompt
from app.strategy.models.test_strategy import TestStrategy


class TestScenarioService:
    def __init__(self, llm_manager: LLMManager):
        self.llm_manager = llm_manager

    def generate_scenarios(
        self,
        analysis: RequirementAnalysis,
        strategy: TestStrategy,
    ) -> ScenarioAnalysis:
        requirement_context = self._build_requirement_context(
            analysis
        )

        risk_strategy_context = self._build_strategy_context(
            strategy
        )

        prompt = build_test_scenario_prompt(
            document_name=analysis.document_name,
            requirement_context=requirement_context,
            risk_strategy_context=risk_strategy_context,
        )

        llm_response = self.llm_manager.generate(
            task_name="scenario",
            prompt=prompt,
        )

        raw_response = self._extract_response_content(
            llm_response
        )

        return self._parse_scenario_response(
            raw_response
        )

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
    def _build_strategy_context(
        strategy: TestStrategy,
    ) -> str:
        lines = [
            f"Strategy Summary: {strategy.strategy_summary}",
            f"Overall Risk Level: {strategy.overall_risk_level.value}",
            (
                "Overall Strategy Confidence: "
                f"{strategy.overall_strategy_confidence}"
            ),
            (
                "Prioritized Requirements: "
                f"{strategy.prioritized_requirements}"
            ),
        ]

        for risk in strategy.requirement_risks:
            lines.append(
                "\n".join(
                    [
                        f"Requirement ID: {risk.requirement_id}",
                        f"Risk Level: {risk.risk_level.value}",
                        f"Risk Score: {risk.risk_score}",
                        f"Risk Reason: {risk.risk_reason}",
                        f"Impacted Areas: {risk.impacted_areas}",
                        (
                            "Recommended Test Types: "
                            f"{[test_type.value for test_type in risk.recommended_test_types]}"
                        ),
                    ]
                )
            )

        return "\n\n--- RISK ENTRY ---\n\n".join(lines)

    @staticmethod
    def _extract_response_content(llm_response) -> str:
        if hasattr(llm_response, "content"):
            content = llm_response.content
        else:
            content = str(llm_response)

        if not content or not content.strip():
            raise ValueError(
                "Test Scenario LLM response is empty."
            )

        return content.strip()

    @staticmethod
    def _parse_scenario_response(
        raw_response: str,
    ) -> ScenarioAnalysis:
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
                        f"Test Scenario response is not valid JSON: {exc}"
                    ) from exc
            else:
                raise ValueError(
                    f"Test Scenario response is not valid JSON: {exc}"
                ) from exc

        try:
            return ScenarioAnalysis.model_validate(data)

        except Exception as exc:
            raise ValueError(
                "Test Scenario response does not conform "
                f"to ScenarioAnalysis schema: {exc}"
            ) from exc
