import json

from app.analysis.models.requirement import RequirementAnalysis
from app.llm.manager import LLMManager
from app.scenario.models.test_scenario import ScenarioAnalysis
from app.scenario.validation.models.review_result import (
    ScenarioReviewResult,
)
from app.scenario.validation.prompts.scenario_validator import (
    build_scenario_validator_prompt,
)
from app.strategy.models.test_strategy import TestStrategy


class ScenarioValidatorService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def validate(
        self,
        analysis: RequirementAnalysis,
        strategy: TestStrategy,
        scenarios: ScenarioAnalysis,
    ) -> ScenarioReviewResult:
        requirement_context = self._build_requirement_context(analysis)
        risk_strategy_context = self._build_strategy_context(strategy)
        scenario_context = self._build_scenario_context(scenarios)

        prompt = build_scenario_validator_prompt(
            document_name=analysis.document_name,
            requirement_context=requirement_context,
            risk_strategy_context=risk_strategy_context,
            scenario_context=scenario_context,
        )

        response = self.llm_manager.generate(
            task_name="scenario_validator",
            prompt=prompt,
        )

        return self._parse_review_response(response.content)

    @staticmethod
    def _build_requirement_context(
        analysis: RequirementAnalysis,
    ) -> str:
        return "\n".join(
            [
                (
                    f"{requirement.requirement_id}: "
                    f"{requirement.title} | "
                    f"{requirement.description} | "
                    f"Type: {requirement.requirement_type} | "
                    f"Classification: {requirement.classification}"
                )
                for requirement in analysis.requirements
            ]
        )

    @staticmethod
    def _build_strategy_context(
        strategy: TestStrategy,
    ) -> str:
        lines = [
            f"Strategy Summary: {strategy.strategy_summary}",
            f"Overall Risk: {strategy.overall_risk_level}",
            f"Strategy Confidence: {strategy.overall_strategy_confidence}",
            (
                "Prioritized Requirements: "
                f"{strategy.prioritized_requirements}"
            ),
        ]

        for risk in strategy.requirement_risks:
            lines.append(
                (
                    f"{risk.requirement_id}: "
                    f"Risk={risk.risk_level}, "
                    f"Score={risk.risk_score}, "
                    f"Reason={risk.risk_reason}, "
                    f"Impacted Areas={risk.impacted_areas}, "
                    f"Recommended Tests={risk.recommended_test_types}"
                )
            )

        return "\n".join(lines)

    @staticmethod
    def _build_scenario_context(
        scenarios: ScenarioAnalysis,
    ) -> str:
        lines = [
            f"Scenario Summary: {scenarios.scenario_summary}",
            (
                "Overall Scenario Confidence: "
                f"{scenarios.overall_scenario_confidence}"
            ),
        ]

        for scenario in scenarios.scenarios:
            lines.append(
                (
                    f"{scenario.scenario_id}: "
                    f"Requirement={scenario.requirement_id}, "
                    f"Title={scenario.title}, "
                    f"Description={scenario.description}, "
                    f"Type={scenario.scenario_type}, "
                    f"Priority={scenario.priority}, "
                    f"Preconditions={scenario.preconditions}, "
                    f"Expected Behavior={scenario.expected_behavior}, "
                    f"Source Requirement={scenario.source_requirement}"
                )
            )

        return "\n".join(lines)

    @staticmethod
    def _parse_review_response(
        content: str,
    ) -> ScenarioReviewResult:
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
        except json.JSONDecodeError:
            start = cleaned.find("{")
            end = cleaned.rfind("}")

            if start == -1 or end == -1 or start >= end:
                raise ValueError(
                    "Scenario validator returned invalid JSON."
                )

            data = json.loads(cleaned[start : end + 1])

        return ScenarioReviewResult.model_validate(data)
