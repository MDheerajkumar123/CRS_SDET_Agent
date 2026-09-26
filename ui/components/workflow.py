"""Workflow cards and live event log."""

from __future__ import annotations

import streamlit as st

from ui.state.session_state import STAGES, progress

_ICONS = {"WAITING": "⌛", "RUNNING": "🔵", "COMPLETED": "✅", "FAILED": "❌", "REWORKING": "🔁"}


def render_workflow(state) -> None:
    value = progress(state)
    st.subheader("Workflow Progress")
    st.progress(value, text=f"{value}% — {sum(c['status'] == 'COMPLETED' for c in state.stage_data.values())} of 12 stages completed")
    for index, stage in enumerate(STAGES, 1):
        card = state.stage_data[stage]
        status = card["status"]
        with st.container(border=True):
            st.markdown(f"**{index:02d} · {stage}** &nbsp; {_ICONS[status]} **{status}**")
            if card.get("provider"):
                st.caption(f"Provider: {card['provider'].title()}  |  Model: {card.get('model', 'Not reported')}")
            if card.get("fallback_provider"):
                st.warning(f"Fallback: {card['primary_provider'].title()} → {card['fallback_provider'].title()}")
            if card.get("score") is not None:
                st.caption(f"Validation score: {card['score']} | Attempt: {card.get('attempt', 0)} / {card.get('max_retries', '—')}")
            if card.get("duration_seconds") is not None:
                st.caption(f"Duration: {card['duration_seconds']} seconds")
            if card.get("message"):
                st.write(card["message"])


def render_logs(events) -> None:
    st.subheader("Live Execution Log")
    lines = [f"{event.timestamp[11:19]}  {event.event_type.replace('_', ' ')}  {event.stage or 'Workflow'} — {event.message}" for event in events[-100:]]
    st.code("\n".join(lines) or "Waiting for workflow events…", language=None)
