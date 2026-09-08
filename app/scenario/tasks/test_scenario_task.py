from crewai import Task

from app.scenario.agents.test_scenario_agent import TestScenarioAgent
from app.scenario.prompts.test_scenario import build_test_scenario_prompt
from app.scenario.models.test_scenario import ScenarioAnalysis


class TestScenarioTask:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
    ):
        self.document_name = document_name
        self.requirement_context = requirement_context
        self.risk_strategy_context = risk_strategy_context

        self.agent = TestScenarioAgent().get_agent()

        self.task = Task(
            description=build_test_scenario_prompt(
                document_name=document_name,
                requirement_context=requirement_context,
                risk_strategy_context=risk_strategy_context,
            ),
            expected_output=(
                "A valid ScenarioAnalysis containing traceable test scenarios "
                "with scenario type, priority, preconditions, expected behavior, "
                "and source requirement."
            ),
            agent=self.agent,
            output_pydantic=ScenarioAnalysis,
        )

    def get_task(self):
        return self.task
