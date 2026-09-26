"""Local real-time UI for the existing CRS SDET backend.

Run with: streamlit run ui/streamlit_app.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from app.orchestrator.workflow import CRSWorkflowInput
from ui.components.dashboard import render_dashboard
from ui.components.workflow import render_logs, render_workflow
from ui.services.event_bus import EventBus
from ui.services.workflow_runner import WorkflowRunner
from ui.state.session_state import STAGES, apply_event, initialise

DEFAULT_QUERY = (
    "Analyze the complete CRS and generate comprehensive, traceable SDET QA artifacts "
    "covering all testable functional requirements, business rules, error and exception "
    "conditions, non-functional requirements, integrations, security, data, dependencies, "
    "risks, scenarios, test design, test cases, RTM coverage, and final QA review."
)
ALLOWED_TYPES = {"docx", "pdf", "txt"}


def _save_upload(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix.lower()
    directory = Path(tempfile.gettempdir()) / "crs_sdet_uploads"
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / f"{uuid4().hex}{suffix}"
    destination.write_bytes(uploaded_file.getvalue())
    return str(destination)


def _consume_events() -> None:
    if st.session_state.event_bus:
        for event in st.session_state.event_bus.drain():
            apply_event(st.session_state, event)


def _reset_run() -> None:
    st.session_state.stage_data = {stage: {"status": "WAITING"} for stage in STAGES}
    st.session_state.events = []
    st.session_state.event_bus = EventBus()
    st.session_state.runner = WorkflowRunner(st.session_state.event_bus)


st.set_page_config(page_title="QAGenesis", page_icon="🧪", layout="wide")
initialise(st.session_state)
st.title("QAGenesis")
st.caption("AI-Powered Requirement Analysis, Test Design and SDET Test Case Generation")

with st.sidebar:
    st.header("Analysis Configuration")
    analysis_query = st.text_area("Analysis Query", value=DEFAULT_QUERY, height=160)
    n_results = st.number_input("n_results", min_value=1, max_value=20, value=5)
    st.caption("Credentials are read only by the existing backend and are never shown here.")

uploaded = st.file_uploader("Upload CRS document", type=sorted(ALLOWED_TYPES))
if uploaded:
    st.caption(f"{uploaded.name} · {uploaded.size:,} bytes")

running = bool(st.session_state.runner and st.session_state.runner.running)
if st.button("Start SDET Analysis", type="primary", disabled=running or not uploaded):
    if uploaded.size == 0:
        st.error("The uploaded document is empty.")
    else:
        _reset_run()
        destination = _save_upload(uploaded)
        output_path = Path("output") / f"crs_sdet_{uuid4().hex}.xlsx"
        st.session_state.runner.start(CRSWorkflowInput(file_path=destination, analysis_query=analysis_query, n_results=int(n_results), output_path=str(output_path)))

_consume_events()
if st.session_state.runner:
    # A fragment can re-run independently, so the long-running worker never
    # causes a full Streamlit rerun or a duplicate workflow launch.
    @st.fragment(run_every=1.0)
    def _live_view():
        _consume_events()
        runner = st.session_state.runner
        if runner.running:
            st.info("Workflow is running. Receiving live backend events…")
        elif runner.error:
            st.error("WORKFLOW FAILED")
            st.write(runner.error)
        elif runner.result:
            st.success("WORKFLOW COMPLETED")
        render_workflow(st.session_state)
        render_logs(st.session_state.events)
        if runner.result:
            render_dashboard(runner.result)
            excel = Path(runner.result.excel_path) if runner.result.excel_path else None
            if excel and excel.is_file():
                st.download_button("Download Excel", data=excel.read_bytes(), file_name=excel.name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.warning("Workflow completed but the Excel output file is unavailable.")
    _live_view()
