from crewai import Crew, Process

from app.validation.tasks.requirement_validation_task import (
    create_requirement_validation_task,
)


class RequirementValidationCrew:
    def __init__(self, analysis_json: str):
        self.task = create_requirement_validation_task(
            analysis_json=analysis_json,
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
