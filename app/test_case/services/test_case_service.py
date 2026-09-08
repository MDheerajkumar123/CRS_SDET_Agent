import json

from app.analysis.models.requirement import RequirementAnalysis
from app.llm.manager import LLMManager
from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.prompts.test_case import build_test_case_prompt


class TestCaseService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def generate_test_cases(
        self,
        analysis: RequirementAnalysis,
        strategy,
        scenario_analysis,
        test_design_analysis,
    ) -> TestCaseAnalysis:
        if not isinstance(analysis, RequirementAnalysis):
            raise TypeError("analysis must be a RequirementAnalysis instance")

        requirement_context = self._build_requirement_context(analysis)
        risk_strategy_context = self._build_strategy_context(strategy)
        scenario_context = self._build_scenario_context(scenario_analysis)
        test_design_context = self._build_test_design_context(
            test_design_analysis
        )

        prompt = build_test_case_prompt(
            document_name=analysis.document_name,
            requirement_context=requirement_context,
            risk_strategy_context=risk_strategy_context,
            scenario_context=scenario_context,
            test_design_context=test_design_context,
        )

        response = self.llm_manager.generate(
            task_name="test_case",
            prompt=prompt,
        )

        return self._parse_response(response.content)

    @staticmethod
    def _build_requirement_context(analysis: RequirementAnalysis) -> str:
        requirements = []

        for requirement in analysis.requirements:
            requirements.append(
                {
                    "requirement_id": requirement.requirement_id,
                    "title": requirement.title,
                    "description": requirement.description,
                    "requirement_type": requirement.requirement_type.value,
                    "classification": requirement.classification.value,
                    "source_section": requirement.source_section,
                    "source_page": requirement.source_page,
                    "source_text": requirement.source_text,
                    "business_rules": requirement.business_rules,
                    "dependencies": requirement.dependencies,
                }
            )

        return json.dumps(requirements, indent=2)

    @staticmethod
    def _build_strategy_context(strategy) -> str:
        return json.dumps(
            strategy.model_dump(),
            indent=2,
        )

    @staticmethod
    def _build_scenario_context(scenario_analysis) -> str:
        return json.dumps(
            scenario_analysis.model_dump(),
            indent=2,
        )

    @staticmethod
    def _build_test_design_context(test_design_analysis) -> str:
        return json.dumps(
            test_design_analysis.model_dump(),
            indent=2,
        )

    @staticmethod
    def _parse_response(content: str) -> TestCaseAnalysis:
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
                "Test Case LLM response is not valid JSON"
            ) from exc

        return TestCaseAnalysis.model_validate(data)
