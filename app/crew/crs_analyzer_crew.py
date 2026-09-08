from crewai import Crew, Process

from app.agents.tasks.crs_analyzer_task import (
    create_crs_analyzer_task,
)


class CRSAnalyzerCrew:
    """
    CrewAI orchestration for CRS requirement analysis.
    """

    def __init__(
        self,
        document_name: str,
        query: str,
        n_results: int = 5,
    ):
        self.task = create_crs_analyzer_task(
            document_name=document_name,
            query=query,
            n_results=n_results,
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
