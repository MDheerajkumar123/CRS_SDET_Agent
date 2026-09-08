from crewai import Crew, Process

from app.scenario.validation.tasks.scenario_validation_task import (
    ScenarioValidationTask,
)


class ScenarioValidationCrew:
    def __init__(
        self,
        document_name,
        requirement_context,
        risk_strategy_context,
        scenario_context,
    ):
        self.task_builder = ScenarioValidationTask(
            document_name=document_name,
            requirement_context=requirement_context,
            risk_strategy_context=risk_strategy_context,
            scenario_context=scenario_context,
        )

        self.task = self.task_builder.get_task()
        self.agent = self.task.agent

    def build(self):
        return Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=True,
        )
