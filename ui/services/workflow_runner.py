"""Background execution adapter for the real CRS workflow."""

from __future__ import annotations

import logging
from threading import Thread
from typing import Callable

from app.observability.events import WorkflowEvent
from app.orchestrator.factory import create_crs_workflow
from app.orchestrator.workflow import CRSWorkflowInput
from ui.services.event_bus import EventBus

logger = logging.getLogger(__name__)


class WorkflowRunner:
    def __init__(self, event_bus: EventBus) -> None:
        self.event_bus = event_bus
        self.thread: Thread | None = None
        self.result = None
        self.error: str | None = None

    @property
    def running(self) -> bool:
        return self.thread is not None and self.thread.is_alive()

    def start(self, workflow_input: CRSWorkflowInput) -> None:
        if self.running:
            raise RuntimeError("A workflow is already running.")
        self.result = None
        self.error = None
        self.thread = Thread(
            target=self._run,
            args=(workflow_input,),
            daemon=True,
            name="crs-sdet-workflow",
        )
        self.thread.start()

    def _run(self, workflow_input: CRSWorkflowInput) -> None:
        try:
            workflow = create_crs_workflow(event_publisher=self.event_bus.publish)
            self.result = workflow.run(workflow_input)
        except Exception as error:  # Details remain in local logs.
            logger.exception("CRS workflow failed")
            self.error = "The backend workflow encountered an error. See the local console for technical details."
            self.event_bus.publish(
                WorkflowEvent(
                    event_type="WORKFLOW_FAILED",
                    message="Workflow failed. See the local console for details.",
                )
            )
