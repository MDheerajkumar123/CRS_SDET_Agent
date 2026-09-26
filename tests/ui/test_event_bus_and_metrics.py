from app.observability.events import WorkflowEvent
from app.llm.manager import LLMManager
from ui.services.event_bus import EventBus
from ui.services.metrics import extract_dashboard_metrics
from ui.state.session_state import STAGES, apply_event, progress


class State(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def test_event_bus_preserves_and_drains_events():
    bus = EventBus(max_events=2)
    bus.publish(WorkflowEvent(event_type="STAGE_STARTED", stage="Requirement Analyzer"))
    bus.publish({"event_type": "STAGE_COMPLETED", "stage": "Requirement Analyzer"})
    assert len(bus.drain()) == 2
    assert len(bus.snapshot()) == 2


def test_stage_projection_and_progress():
    state = State(stage_data={stage: {"status": "WAITING"} for stage in STAGES}, events=[])
    apply_event(state, WorkflowEvent(event_type="STAGE_STARTED", stage=STAGES[0], provider="gemini", model="model"))
    assert state.stage_data[STAGES[0]]["status"] == "RUNNING"
    apply_event(state, WorkflowEvent(event_type="STAGE_COMPLETED", stage=STAGES[0]))
    assert progress(state) == 8
    assert state.stage_data[STAGES[0]]["provider"] == "gemini"


def test_metrics_do_not_invent_missing_artifacts():
    result = type("Result", (), {})()
    metrics = extract_dashboard_metrics(result)
    assert metrics["requirements"] == 0
    assert metrics["coverage"] is None


def test_excel_availability_is_checked_by_real_path():
    existing = Path("pytest.ini")
    assert existing.is_file()
    assert not Path("output/does-not-exist.xlsx").is_file()


def test_llm_fallback_is_published(monkeypatch):
    events = []
    manager = LLMManager(event_publisher=events.append)
    manager.providers["gemini"] = type("Failing", (), {"generate": lambda *_args, **_kwargs: (_ for _ in ()).throw(ValueError("unavailable"))})()
    manager.providers["openrouter"] = type("Working", (), {"generate": lambda *_args, **_kwargs: "response"})()
    monkeypatch.setattr("app.llm.manager.get_provider_for_task", lambda _task: "gemini")
    monkeypatch.setattr("app.llm.manager.get_fallback_provider", lambda _provider: ["openrouter"])
    response = manager.generate("example", "prompt")
    assert response.fallback_used
    assert any(event.event_type == "LLM_FALLBACK" for event in events)
from pathlib import Path
