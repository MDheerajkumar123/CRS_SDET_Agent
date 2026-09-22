def build_scenario_rework_prompt(
    document_name: str,
    current_scenarios: str,
    issues: list[str],
    required_changes: list[str],
    retry_count: int,
    risk_strategy_context: str,
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

RISK & TEST STRATEGY CONTEXT:
{risk_strategy_context}

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

7. IMPORTANT: scenario_type must be ONLY one of these exact values:
    Positive, Negative, Boundary, Error, Integration, Security,
    Performance, Reliability, Usability, Compatibility, Regression.

    Auditability is NOT a valid scenario_type.
    Functional is NOT a valid scenario_type.
    Auditability, Functional, and other test types/domains must never
    be used as scenario_type values.

    If a scenario concerns auditability, select the scenario_type
    that best represents the testing behavior, such as Security,
    Integration, Positive, Negative, or Regression.

8. Maintain appropriate positive, negative, boundary, error,
   integration, security, performance, usability, compatibility,
   and regression coverage where supported by the requirements.

9. Do not remove valid risk-based coverage merely to reduce the
   number of scenarios.

10. Do not introduce unsupported assumptions during rework.

11. OUTPUT SIZE RULES:
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

12. Return the complete revised ScenarioAnalysis, not only the
    changed scenarios.

13. STRICT JSON SCHEMA AND DATA TYPES:

    The final response MUST conform exactly to the ScenarioAnalysis
    schema.

    ScenarioAnalysis:
    {
      "document_name": "string",
      "scenario_summary": "string",
      "scenarios": [
        {
          "scenario_id": "string",
          "requirement_id": "string",
          "title": "string",
          "description": "string",
          "scenario_type": "string",
          "priority": "string",
          "preconditions": ["string"],
          "expected_behavior": "string",
          "source_requirement": "string"
        }
      ],
      "overall_scenario_confidence": "number between 0 and 1"
    }

    STRICT TYPE RULES:
    - document_name MUST be a string.
    - scenario_summary MUST be a string.
    - scenarios MUST be an array of objects.
    - scenario_id MUST be a string.
    - requirement_id MUST be a string.
    - title MUST be a string.
    - description MUST be a string.
    - scenario_type MUST be a string using only the allowed
      ScenarioType values defined above.
    - priority MUST be a string.
    - preconditions MUST be an array of strings.
    - expected_behavior MUST be ONE STRING, never an array.
    - source_requirement MUST be a string.
    - overall_scenario_confidence MUST be a number between 0 and 1.

    IMPORTANT:
    - NEVER return expected_behavior as a JSON array.
    - If multiple expected behaviors are needed, combine them into
      ONE concise string.
    - Example of VALID:
      "System processes the refund within the documented policy and
      records the refund transaction correctly."
    - Example of INVALID:
      "expected_behavior": [
        "System processes the refund.",
        "System records the refund."
      ]

14. OUTPUT FORMAT:
    - Return ONLY valid JSON.
    - Do NOT include Markdown code fences.
    - Do NOT include explanatory text before or after the JSON.
    - Do NOT include comments such as // or /* ... */ inside the JSON.
    - Use double quotes for all JSON keys and string values.
    - The response must be directly parseable by Python json.loads().
    - The JSON MUST conform to the ScenarioAnalysis schema above.

The revised scenarios must be ready for another independent
validation review.
""".strip()