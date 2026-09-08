from app.final_review.services.final_qa_rework_dispatcher import (
    FinalQAReworkDispatcher,
)


class FakeHandler:
    pass


def make_dispatcher():
    return FinalQAReworkDispatcher(
        requirement_handler=FakeHandler(),
        risk_strategy_handler=FakeHandler(),
        scenario_handler=FakeHandler(),
        test_design_handler=FakeHandler(),
        test_case_handler=FakeHandler(),
        rtm_handler=FakeHandler(),
    )


def test_dispatcher_returns_correct_handler_for_all_artifacts():
    requirement_handler = FakeHandler()
    risk_strategy_handler = FakeHandler()
    scenario_handler = FakeHandler()
    test_design_handler = FakeHandler()
    test_case_handler = FakeHandler()
    rtm_handler = FakeHandler()

    dispatcher = FinalQAReworkDispatcher(
        requirement_handler=requirement_handler,
        risk_strategy_handler=risk_strategy_handler,
        scenario_handler=scenario_handler,
        test_design_handler=test_design_handler,
        test_case_handler=test_case_handler,
        rtm_handler=rtm_handler,
    )

    assert (
        dispatcher.get_handler("REQUIREMENTS")
        is requirement_handler
    )

    assert (
        dispatcher.get_handler("RISK_STRATEGY")
        is risk_strategy_handler
    )

    assert (
        dispatcher.get_handler("SCENARIOS")
        is scenario_handler
    )

    assert (
        dispatcher.get_handler("TEST_DESIGNS")
        is test_design_handler
    )

    assert (
        dispatcher.get_handler("TEST_CASES")
        is test_case_handler
    )

    assert (
        dispatcher.get_handler("RTM")
        is rtm_handler
    )


def test_dispatcher_rejects_unknown_artifact():
    dispatcher = make_dispatcher()

    try:
        dispatcher.get_handler("UNKNOWN")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "No Final QA rework handler registered" in str(exc)


def test_dispatcher_rejects_non_string_artifact():
    dispatcher = make_dispatcher()

    try:
        dispatcher.get_handler(None)
        assert False, "Expected TypeError"
    except TypeError as exc:
        assert "artifact must be a string" in str(exc)
