from app.llm.manager import LLMManager
from app.scenario.parsers.scenario_parser import ScenarioAnalysisParser
from app.scenario.models.test_scenario import ScenarioAnalysis
from app.scenario.validation.models.review_result import (
    ScenarioReviewResult,
)
from app.scenario.validation.prompts.rework_prompt import (
    build_scenario_rework_prompt,
)


class ScenarioReworkService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def rework(
        self,
        scenarios: ScenarioAnalysis,
        review: ScenarioReviewResult,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        retry_count: int = 0,
        ) -> tuple[ScenarioAnalysis, object]:

        if not isinstance(scenarios, ScenarioAnalysis):
            raise TypeError(
                "scenarios must be a ScenarioAnalysis instance."
            )

        if not isinstance(review, ScenarioReviewResult):
            raise TypeError(
                "review must be a ScenarioReviewResult instance."
            )

        if review.status.value != "REWORK":
            raise ValueError(
                "Rework can only be performed when review status is REWORK."
            )

        current_scenarios = scenarios.model_dump_json(indent=2)

        prompt = build_scenario_rework_prompt(
            document_name=document_name,
            current_scenarios=current_scenarios,
            issues=review.issues,
            required_changes=review.required_changes,
            retry_count=retry_count,
            risk_strategy_context=risk_strategy_context,
        )

        llm_response = self.llm_manager.generate(
            task_name="scenario",
            prompt=prompt,
        )

        print("\n=== SCENARIO REWORK RAW RESPONSE ===")
        print(repr(llm_response.content))
        print("=== END SCENARIO REWORK RAW RESPONSE ===\n")

        revised_scenarios = ScenarioAnalysisParser.parse(
            llm_response.content
        )

        return revised_scenarios, llm_response
