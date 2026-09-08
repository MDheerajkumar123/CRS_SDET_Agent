
def build_final_qa_rework_prompt(
    document_name: str,
    requirement_context: str,
    risk_strategy_context: str,
    scenario_context: str,
    test_design_context: str,
    test_case_context: str,
    rtm_context: str,
    issues: list[str],
    required_changes: list[str],
    retry_count: int,
) -> str:
    return f"""
You are coordinating rework for the Final QA Review of a CRS-based
Senior SDET QA package.

Document:
{document_name}

Current Requirements:
{requirement_context}

Current Risk and Test Strategy:
{risk_strategy_context}

Current Test Scenarios:
{scenario_context}

Current Test Designs:
{test_design_context}

Current Test Cases:
{test_case_context}

Current RTM:
{rtm_context}

Final QA Reviewer Issues:
{issues}

Final QA Reviewer Required Changes:
{required_changes}

Retry Count:
{retry_count}

Your task is to determine the appropriate upstream QA artifacts that
must be corrected based on the final reviewer findings.

IMPORTANT PRINCIPLES:

1. Do not invent requirements.
2. Do not invent business rules.
3. Do not invent requirement IDs.
4. Do not invent scenario IDs.
5. Do not invent test design IDs.
6. Do not invent test case IDs.
7. Do not invent RTM relationships.
8. Preserve all valid source-supported information.
9. Do not change requirements merely to make downstream coverage appear better.
10. Do not create unsupported security, performance, integration, or other
    test expectations.
11. Rework only the artifact areas affected by the reviewer findings.
12. Prefer correcting the lowest-level affected QA artifact when possible.
13. If a risk strategy gap affects scenarios, identify the scenario artifact
    for rework.
14. If a scenario gap affects test designs, identify the test design artifact
    for rework.
15. If a test case gap affects RTM coverage, identify the test case and/or
    RTM artifact for rework as appropriate.
16. Preserve end-to-end traceability after rework.
17. RTM coverage must remain evidence-based.
18. Do not inflate coverage percentages.
19. Do not introduce implementation details, tools, credentials,
    environments, APIs, infrastructure, or execution capabilities that
    are not supported by the source artifacts.
20. Stay within the V1 QA scope.
21. If an issue cannot be corrected from the supplied evidence, identify it
    clearly rather than inventing a solution.

UPSTREAM REWORK TARGETS:

- REQUIREMENTS
  Use only when the reviewer identifies a requirement completeness,
  classification, ambiguity, source-fidelity, or requirement-level issue.

- RISK_STRATEGY
  Use when risk levels, risk reasoning, impacted areas, or recommended
  test types are inconsistent with the requirements.

- SCENARIOS
  Use when scenario coverage, scenario types, scenario traceability,
  or risk-aligned scenario coverage is insufficient.

- TEST_DESIGNS
  Use when test design techniques, conditions, coverage areas, or
  scenario-to-design traceability are insufficient.

- TEST_CASES
  Use when test steps, expected results, test data, test types,
  priorities, testability, or design-to-test-case traceability are
  insufficient.

- RTM
  Use when requirement coverage classification, traceability,
  coverage counts, coverage percentage, or RTM evidence is incorrect.

For each reviewer issue, determine the most appropriate rework target(s).

OUTPUT RULES:

- Return valid JSON only.
- Do not use Markdown code fences.
- Do not include commentary outside JSON.
- Keep the result concise and actionable.
- Do not generate replacement requirements or test cases in this step.
- This step identifies the correct rework targets and actions.

Required JSON structure:

{{
  "document_name": "string",
  "rework_targets": [
    {{
      "artifact": "REQUIREMENTS | RISK_STRATEGY | SCENARIOS | TEST_DESIGNS | TEST_CASES | RTM",
      "reason": "string",
      "actions": [
        "string"
      ]
    }}
  ],
  "overall_rework_summary": "string"
}}
""".strip()
