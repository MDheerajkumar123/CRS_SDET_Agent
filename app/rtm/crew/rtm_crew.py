
from crewai import Crew, Process

from app.rtm.tasks.rtm_task import create_rtm_task


class RTMCrew:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_context: str,
    ):
        self.task = create_rtm_task(
            document_name=document_name,
            requirement_context=requirement_context,
            scenario_context=scenario_context,
            test_design_context=test_design_context,
            test_case_context=test_case_context,
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
