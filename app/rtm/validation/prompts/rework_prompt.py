
def build_rtm_rework_prompt(
    document_name: str,
    current_rtm: str,
    issues: list[str],
    required_changes: list[str],
    retry_count: int,
) -> str:
    return f"""
You are reworking a Requirements Traceability Matrix (RTM) for a
Senior SDET / QA workflow.

Document:
{document_name}

Current RTM:
{current_rtm}

Reviewer Issues:
{issues}

Required Changes:
{required_changes}

Retry Count:
{retry_count}

Your task is to produce a complete revised RTMAnalysis.

STRICT RULES:

1. Preserve valid information from the current RTM.
2. Correct every issue identified by the reviewer.
3. Apply every required change.
4. Do not invent requirement IDs.
5. Do not invent scenario IDs.
6. Do not invent test design IDs.
7. Do not invent test case IDs.
8. Every relationship must be supported by the supplied QA artifacts.
9. Do not create unsupported requirement-to-scenario relationships.
10. Do not create unsupported scenario-to-design relationships.
11. Do not create unsupported design-to-test-case relationships.
12. Preserve end-to-end traceability.
13. Recalculate Covered, Partial, and Not Covered classifications based
    only on available evidence.
14. Recalculate coverage counts.
15. Recalculate overall coverage percentage using:

    (Covered + 0.5 * Partial) / Total Requirements * 100

16. Ensure every requirement is evaluated.
17. Do not force requirements to Covered merely to increase the percentage.
18. Use Partial when evidence exists but complete traceability is not established.
19. Use Not Covered when no valid downstream evidence exists.
20. Keep coverage notes concise and evidence-based.
21. Do not introduce implementation details that are not present in the
    supplied source artifacts.
22. Stay within the V1 QA scope.
23. Return the complete RTMAnalysis, not only the changed rows.
24. Output valid JSON only.
25. Do not use Markdown code fences.

Required JSON structure:

{{
  "document_name": "string",
  "rtm_summary": "string",
  "requirement_coverage": [
    {{
      "requirement_id": "string",
      "scenario_ids": [],
      "design_ids": [],
      "test_case_ids": [],
      "coverage_status": "Covered | Partial | Not Covered",
      "coverage_notes": "string"
    }}
  ],
  "total_requirements": 0,
  "covered_requirements": 0,
  "partially_covered_requirements": 0,
  "not_covered_requirements": 0,
  "overall_coverage_percentage": 0.0
}}
""".strip()
