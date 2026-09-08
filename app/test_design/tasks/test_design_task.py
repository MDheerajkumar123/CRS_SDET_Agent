from crewai import Task

from app.test_design.agents.test_design_agent import TestDesignAgent
from app.test_design.models.test_design import TestDesignAnalysis


class TestDesignTask:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        scenario_context: str,
    ):
        self.document_name = document_name
        self.requirement_context = requirement_context
        self.risk_strategy_context = risk_strategy_context
        self.scenario_context = scenario_context

    def create_task(self) -> Task:
        agent = TestDesignAgent().get_agent()

        description = f"""
        Create structured test designs for the validated test scenarios.

        Document:
        {self.document_name}

        Validated Requirements:
        {self.requirement_context}

        Validated Risk & Test Strategy:
        {self.risk_strategy_context}

        Validated Test Scenarios:
        {self.scenario_context}

        Produce traceable, risk-based test designs using appropriate
        test design techniques.

        Do not invent requirements, business rules, workflows, values,
        APIs, databases, implementation details, or execution steps.

        Return the complete TestDesignAnalysis structure.
        """

        return Task(
            description=description.strip(),
            expected_output=(
                "A valid TestDesignAnalysis containing traceable and "
                "risk-based test designs."
            ),
            agent=agent,
            output_pydantic=TestDesignAnalysis,
        )
