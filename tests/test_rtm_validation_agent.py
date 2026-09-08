
from app.rtm.validation.agents.rtm_validation_agent import (
    RTMValidationAgent,
)


def test_rtm_validation_agent_construction():
    agent_wrapper = RTMValidationAgent()

    assert agent_wrapper.agent is not None
    assert agent_wrapper.agent.role == "Senior SDET RTM Validation Reviewer"
    assert agent_wrapper.agent.allow_delegation is False
