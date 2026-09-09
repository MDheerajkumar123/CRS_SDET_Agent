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

6a. IMPORTANT: scenario_type must be ONLY one of these exact values:
    Positive, Negative, Boundary, Error, Integration, Security,
    Performance, Reliability, Usability, Compatibility, Regression.

    Auditability is NOT a valid scenario_type.
    Functional is NOT a valid scenario_type.
    Auditability, Functional, and other test types/domains must never
    be used as scenario_type values.

    If a scenario concerns auditability, select the scenario_type
    that best represents the testing behavior, such as Security,
    Integration, Positive, Negative, or Regression.

7. Maintain appropriate positive, negative, boundary, error,
   integration, security, performance, usability, compatibility,
   and regression coverage where supported by the requirements.

8. Do not remove valid risk-based coverage merely to reduce the
   number of scenarios.

9. Do not introduce unsupported assumptions during rework.

10. OUTPUT SIZE RULES:
    - Preserve existing valid scenarios wherever possible.
    - Do not regenerate the entire scenario suite unnecessarily.
    - Add only the minimum scenarios required to address the
      validator findings.
    - The final ScenarioAnalysis MUST contain no more than 18 scenarios.
    - Prefer 1 to 2 scenarios per requirement.
    - Critical and High-risk requirements may have up to 2 scenarios.
    - Do not create duplicate scenarios when existing scenarios
      already provide the required coverage.
    - Keep descriptions, preconditions, and expected behavior concise.

11. Return the complete revised ScenarioAnalysis, not only the
    changed scenarios.

12. OUTPUT FORMAT:
    - Return ONLY valid JSON.
    - Do NOT include Markdown code fences.
    - Do NOT include explanatory text before or after the JSON.
    - Do NOT include comments such as // or /* ... */ inside the JSON.
    - Use double quotes for all JSON keys and string values.
    - The response must be directly parseable by Python json.loads().

The revised scenarios must be ready for another independent
validation review.
""".strip()