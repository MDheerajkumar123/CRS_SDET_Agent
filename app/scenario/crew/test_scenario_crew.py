from crewai import Crew, Process

from app.scenario.tasks.test_scenario_task import TestScenarioTask


class TestScenarioCrew:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
    ):
        self.task_builder = TestScenarioTask(
            document_name=document_name,
            requirement_context=requirement_context,
            risk_strategy_context=risk_strategy_context,
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
