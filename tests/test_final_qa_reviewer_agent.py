
from app.final_review.agents.final_qa_reviewer_agent import (
    FinalQAReviewerAgent,
)


def test_final_qa_reviewer_agent_construction():
    agent_wrapper = FinalQAReviewerAgent()

    assert agent_wrapper.agent is not None
    assert agent_wrapper.agent.role == "Senior SDET Final QA Reviewer"
    assert agent_wrapper.agent.allow_delegation is False
