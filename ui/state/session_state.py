"""Session state defaults and event-to-card projection."""

from __future__ import annotations

from app.observability.events import WorkflowEvent

STAGES = [
    "Requirement Analyzer", "Requirement Validator", "Risk & Test Strategy",
    "Scenario Generator", "Scenario Validator", "Test Design",
    "Test Case Generator", "Test Case Validator", "RTM Generator",
    "RTM Validator", "Final QA Reviewer", "Excel Generator",
]


def initialise(state) -> None:
    state.setdefault("stage_data", {stage: {"status": "WAITING"} for stage in STAGES})
    state.setdefault("events", [])
    state.setdefault("runner", None)
    state.setdefault("event_bus", None)


def apply_event(state, event: WorkflowEvent) -> None:
    state.events.append(event)
    state.events = state.events[-500:]
    if event.stage not in state.stage_data:
        return
    card = state.stage_data[event.stage]
    if event.event_type == "STAGE_STARTED":
        card["status"] = "RUNNING"
    elif event.event_type == "STAGE_COMPLETED":
        card["status"] = "COMPLETED"
    elif event.event_type == "STAGE_FAILED":
        card["status"] = "FAILED"
    elif event.event_type == "REWORK_STARTED":
        card["status"] = "REWORKING"
    card.update({key: value for key, value in {
        "provider": event.provider, "model": event.model,
        "message": event.message, **event.metadata,
    }.items() if value is not None and value != ""})


def progress(state) -> int:
    return round(100 * sum(card["status"] == "COMPLETED" for card in state.stage_data.values()) / len(STAGES))
