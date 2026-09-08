def build_scenario_rework_prompt(
    document_name: str,
    current_scenarios: str,
    issues: list[str],
    required_changes: list[str],
    retry_count: int,
) -> str:

    issues_text = "\n".join(
        f"- {issue}" for issue in issues
    ) or "- None"

    changes_text = "\n".join(
        f"- {change}" for change in required_changes
    ) or "- None"

    return f"""
You are revising test scenarios for the document: {document_name}

This is rework attempt {retry_count}.

CURRENT TEST SCENARIOS:
{current_scenarios}

VALIDATOR ISSUES:
{issues_text}

REQUIRED CHANGES:
{changes_text}

REWORK INSTRUCTIONS:

1. Fix every issue identified by the validator.
2. Apply every required change.
3. Preserve valid scenarios that do not require modification.
4. Maintain traceability to the original requirements.
5. Do not invent requirements, business rules, values, workflows,
   integrations, or implementation details.
6. Ensure each scenario has:
   - scenario ID
   - requirement ID
   - title
   - description
   - scenario type
   - priority
   - preconditions
   - expected behavior
   - source requirement
7. Maintain appropriate positive, negative, boundary, error,
   integration, security, performance, usability, compatibility,
   and regression coverage where supported by the requirements.
8. Do not remove valid risk-based coverage merely to reduce the
   number of scenarios.
9. Do not introduce unsupported assumptions during rework.
10. Return the complete revised ScenarioAnalysis, not only the
    changed scenarios.

The revised scenarios must be ready for another independent
validation review.
""".strip()
