from app.analysis.models.requirement import RequirementAnalysis
from app.llm.manager import LLMManager
from app.strategy.models.test_strategy import TestStrategy
from app.test_design.models.test_design import TestDesignAnalysis
from app.test_design.prompts.test_design import build_test_design_prompt


class TestDesignService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def generate_designs(
        self,
        analysis: RequirementAnalysis,
        strategy: TestStrategy,
        scenario_analysis,
    ) -> TestDesignAnalysis:
        if not isinstance(analysis, RequirementAnalysis):
            raise TypeError(
                "analysis must be a RequirementAnalysis instance."
            )

        if not isinstance(strategy, TestStrategy):
            raise TypeError(
                "strategy must be a TestStrategy instance."
            )

        requirement_context = self._build_requirement_context(analysis)
        risk_strategy_context = self._build_strategy_context(strategy)
        scenario_context = self._build_scenario_context(scenario_analysis)

        prompt = build_test_design_prompt(
            document_name=analysis.document_name,
            requirement_context=requirement_context,
            risk_strategy_context=risk_strategy_context,
            scenario_context=scenario_context,
        )

        response = self.llm_manager.generate(
            task_name="test_design",
            prompt=prompt,
        )

        return self._parse_response(response.content)

    @staticmethod
    def _build_requirement_context(
        analysis: RequirementAnalysis,
    ) -> str:
        lines = []

        for requirement in analysis.requirements:
            lines.append(
                f"Requirement ID: {requirement.requirement_id}\n"
                f"Title: {requirement.title}\n"
                f"Type: {requirement.requirement_type.value}\n"
                f"Classification: {requirement.classification.value}\n"
                f"Description: {requirement.description}\n"
                f"Source Section: {requirement.source_section}\n"
                f"Source Text: {requirement.source_text}"
            )

        return "\n\n".join(lines)

    @staticmethod
    def _build_strategy_context(
        strategy: TestStrategy,
    ) -> str:
        lines = []

        for risk in strategy.requirement_risks:
            test_types = ", ".join(
                test_type.value
                for test_type in risk.recommended_test_types
            )

            lines.append(
                f"Requirement ID: {risk.requirement_id}\n"
                f"Risk Level: {risk.risk_level.value}\n"
                f"Risk Score: {risk.risk_score}\n"
                f"Risk Reason: {risk.risk_reason}\n"
                f"Impacted Areas: {', '.join(risk.impacted_areas)}\n"
                f"Recommended Test Types: {test_types}"
            )

        return "\n\n".join(lines)

    @staticmethod
    def _build_scenario_context(
        scenario_analysis,
    ) -> str:
        lines = []

        for scenario in scenario_analysis.scenarios:
            lines.append(
                f"Scenario ID: {scenario.scenario_id}\n"
                f"Requirement ID: {scenario.requirement_id}\n"
                f"Title: {scenario.title}\n"
                f"Description: {scenario.description}\n"
                f"Scenario Type: {scenario.scenario_type.value}\n"
                f"Priority: {scenario.priority}\n"
                f"Preconditions: {', '.join(scenario.preconditions)}\n"
                f"Expected Behavior: {scenario.expected_behavior}\n"
                f"Source Requirement: {scenario.source_requirement}"
            )

        return "\n\n".join(lines)

    @staticmethod
    def _parse_response(raw_response: str) -> TestDesignAnalysis:
        import json

        if not raw_response or not raw_response.strip():
            raise ValueError("LLM response is empty.")

        cleaned_response = raw_response.strip()

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
            raise ValueError(
                f"LLM response is not valid JSON: {exc}"
            ) from exc

        try:
            return TestDesignAnalysis.model_validate(data)
        except Exception as exc:
            raise ValueError(
                f"LLM JSON does not conform to TestDesignAnalysis "
                f"schema: {exc}"
            ) from exc
