
from app.rtm.agents.rtm_agent import RTMAgent


def test_rtm_agent_construction():
    rtm_agent = RTMAgent()

    agent = rtm_agent.get_agent()

    assert agent is not None
    assert agent.role == "Senior SDET RTM and Coverage Analyst"
    assert agent.allow_delegation is False

    print("RTM agent construction PASS")
