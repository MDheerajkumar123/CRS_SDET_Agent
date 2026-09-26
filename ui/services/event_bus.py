"""Thread-safe event transport used by the local Streamlit worker."""

from __future__ import annotations

from queue import Empty, Queue
from threading import Lock
from typing import Any

from app.observability.events import WorkflowEvent


class EventBus:
    """Keep a bounded history while making new events available to the UI."""

    def __init__(self, max_events: int = 500) -> None:
        self._queue: Queue[WorkflowEvent] = Queue()
        self._events: list[WorkflowEvent] = []
        self._max_events = max_events
        self._lock = Lock()

    def publish(self, event: WorkflowEvent | dict[str, Any]) -> None:
        if isinstance(event, dict):
            event = WorkflowEvent(**event)
        with self._lock:
            self._events.append(event)
            del self._events[:-self._max_events]
        self._queue.put(event)

    def drain(self) -> list[WorkflowEvent]:
        items: list[WorkflowEvent] = []
        while True:
            try:
                items.append(self._queue.get_nowait())
            except Empty:
                return items

    def snapshot(self) -> list[WorkflowEvent]:
        with self._lock:
            return list(self._events)
