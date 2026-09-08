
from crewai import Crew, Process

from app.rtm.validation.tasks.rtm_validation_task import (
    create_rtm_validation_task,
)


class RTMValidationCrew:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_context: str,
        rtm_context: str,
    ):
        self.task = create_rtm_validation_task(
            document_name=document_name,
            requirement_context=requirement_context,
            scenario_context=scenario_context,
            test_design_context=test_design_context,
            test_case_context=test_case_context,
            rtm_context=rtm_context,
        )

        self.crew = Crew(
            agents=[self.task.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=True,
        )

    def get_crew(self) -> Crew:
        return self.crew

    def kickoff(self):
        return self.crew.kickoff()
