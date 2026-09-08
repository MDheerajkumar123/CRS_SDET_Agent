from crewai import Task

from app.scenario.validation.agents.scenario_validation_agent import (
    ScenarioValidationAgent,
)
from app.scenario.validation.prompts.scenario_validator import (
    build_scenario_validator_prompt,
)
from app.scenario.validation.models.review_result import (
    ScenarioReviewResult,
)


class ScenarioValidationTask:
    def __init__(
        self,
        document_name,
        requirement_context,
        risk_strategy_context,
        scenario_context,
    ):
        self.document_name = document_name
        self.requirement_context = requirement_context
        self.risk_strategy_context = risk_strategy_context
        self.scenario_context = scenario_context

        self.agent = ScenarioValidationAgent().get_agent()

        self.task = Task(
            description=build_scenario_validator_prompt(
                document_name=document_name,
                requirement_context=requirement_context,
                risk_strategy_context=risk_strategy_context,
                scenario_context=scenario_context,
            ),
            expected_output=(
                "A valid ScenarioReviewResult containing status, score, "
                "issues, and required_changes."
            ),
            agent=self.agent,
            output_pydantic=ScenarioReviewResult,
        )

    def get_task(self):
        return self.task
