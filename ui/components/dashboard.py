"""Result dashboard based solely on returned workflow artifacts."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from ui.services.metrics import extract_dashboard_metrics


def _chart(title: str, values: dict[str, int]) -> None:
    if values:
        st.caption(title)
        st.bar_chart(pd.DataFrame.from_dict(values, orient="index", columns=["Count"]))
    else:
        st.caption(f"{title}: Not available")


def render_dashboard(result) -> None:
    metrics = extract_dashboard_metrics(result)
    st.subheader("Final QA / SDET Dashboard")
    first, second, third, fourth = st.columns(4)
    first.metric("Requirements", metrics["requirements"])
    second.metric("Scenarios", metrics["scenarios"])
    third.metric("Test Cases", metrics["test_cases"])
    fourth.metric("RTM Entries", metrics["rtm_entries"])
    if metrics["coverage"] is not None:
        st.info(f"RTM coverage: {metrics['covered_requirements']} / {metrics['total_requirements']} ({metrics['coverage']:.1f}%)")
    left, right = st.columns(2)
    with left:
        _chart("Requirement Type Distribution", metrics["requirement_types"])
        _chart("Scenario Type Distribution", metrics["scenario_types"])
        _chart("Test Case Type Distribution", metrics["test_case_types"])
    with right:
        _chart("Requirement Classification", metrics["requirement_classifications"])
        _chart("Test Design Technique Distribution", metrics["design_techniques"])
        _chart("Risk Distribution", metrics["risk_distribution"])
