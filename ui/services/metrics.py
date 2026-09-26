"""Extract only directly available metrics from workflow artifacts."""

from __future__ import annotations

from collections import Counter
from typing import Any


def _values(items: Any, attribute: str) -> dict[str, int]:
    values = [str(getattr(item, attribute)) for item in (items or []) if getattr(item, attribute, None) is not None]
    return dict(Counter(values))


def extract_dashboard_metrics(result: Any) -> dict[str, Any]:
    requirements = getattr(getattr(result, "requirement_analysis", None), "requirements", [])
    scenarios = getattr(getattr(result, "scenario_analysis", None), "scenarios", [])
    designs = getattr(getattr(result, "test_design_analysis", None), "test_designs", [])
    cases = getattr(getattr(result, "test_case_analysis", None), "test_cases", [])
    rtm = getattr(result, "rtm_analysis", None)
    rtm_entries = getattr(rtm, "requirement_coverage", [])
    strategy = getattr(result, "test_strategy", None)
    risks = getattr(strategy, "requirement_risks", [])
    covered = getattr(rtm, "covered_requirements", 0) if rtm else 0
    total = getattr(rtm, "total_requirements", 0) if rtm else 0
    return {
        "requirements": len(requirements), "scenarios": len(scenarios),
        "test_cases": len(cases), "rtm_entries": len(rtm_entries),
        "coverage": getattr(rtm, "overall_coverage_percentage", None) if rtm else None,
        "covered_requirements": covered, "total_requirements": total,
        "requirement_types": _values(requirements, "requirement_type"),
        "requirement_classifications": _values(requirements, "classification"),
        "scenario_types": _values(scenarios, "scenario_type"),
        "test_case_types": _values(cases, "test_type"),
        "design_techniques": _values(designs, "test_design_technique"),
        "risk_distribution": _values(risks, "risk_level"),
    }
