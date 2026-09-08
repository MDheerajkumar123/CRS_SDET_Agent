
def build_rtm_prompt(
    document_name: str,
    requirement_context: str,
    scenario_context: str,
    test_design_context: str,
    test_case_context: str,
) -> str:
    return f"""
You are a Senior SDET responsible for creating a Requirement Traceability
Matrix (RTM) for the document below.

DOCUMENT:
{document_name}

Your objective is to establish deterministic traceability:

Requirement
    ↓
Test Scenario
    ↓
Test Design
    ↓
Test Case

SOURCE REQUIREMENTS:
{requirement_context}

TEST SCENARIOS:
{scenario_context}

TEST DESIGNS:
{test_design_context}

TEST CASES:
{test_case_context}

RTM RULES:

1. Requirement traceability
- Every requirement must be evaluated.
- Use only requirement IDs present in the supplied requirement context.
- Do not invent requirement IDs.

2. Scenario traceability
- Link each requirement only to scenario IDs that actually correspond
  to that requirement.
- Use only scenario IDs present in the supplied scenario context.
- Do not invent scenario IDs.

3. Test design traceability
- Link designs only when their scenario and requirement relationships
  are supported by the supplied context.
- Use only design IDs present in the supplied test design context.
- Do not invent design IDs.

4. Test case traceability
- Link test cases only when their design, scenario, and requirement
  relationships are supported by the supplied context.
- Use only test case IDs present in the supplied test case context.
- Do not invent test case IDs.

5. Coverage classification
Classify every requirement as exactly one of:
- Covered
- Partial
- Not Covered

Covered:
A valid requirement → scenario → design → test case traceability chain
exists.

Partial:
Some traceability exists, but coverage is incomplete or the complete
chain cannot be established.

Not Covered:
No valid test coverage can be established.

6. No hallucination
- Never create IDs that are not present in the source contexts.
- Never assume a relationship simply because two IDs look similar.
- Do not invent implementation details, test execution results,
  environments, tools, data, or system behavior.
- If evidence is insufficient, mark the requirement as Partial or
  Not Covered and explain why.

7. Completeness
- Include every supplied requirement exactly once in the RTM.
- Do not omit requirements.
- Do not create duplicate requirement coverage records.

8. Coverage calculation
Calculate:
- total_requirements
- covered_requirements
- partially_covered_requirements
- not_covered_requirements
- overall_coverage_percentage

Coverage percentage must be:

(
    covered_requirements
    + 0.5 * partially_covered_requirements
)
/
total_requirements
* 100

If total_requirements is zero, coverage percentage must be 0.

9. Evidence-based notes
For each requirement, provide concise coverage notes explaining:
- why it is Covered, Partial, or Not Covered
- important traceability gaps, if any

10. Scope
This is an RTM and coverage analysis only.
Do not generate new test cases.
Do not generate test execution results.
Do not generate defects.
Do not generate automation code.

OUTPUT REQUIREMENT:

Return ONLY valid JSON.

The JSON must follow this structure:

{{
    "document_name": "{document_name}",
    "rtm_summary": "Brief evidence-based RTM summary",
    "requirement_coverage": [
        {{
            "requirement_id": "REQ-001",
            "scenario_ids": ["SCN-001"],
            "design_ids": ["TD-001"],
            "test_case_ids": ["TC-001"],
            "coverage_status": "Covered",
            "coverage_notes": "Complete requirement to test case traceability."
        }}
    ],
    "total_requirements": 1,
    "covered_requirements": 1,
    "partially_covered_requirements": 0,
    "not_covered_requirements": 0,
    "overall_coverage_percentage": 100.0
}}

Do not wrap the JSON in Markdown fences.
Do not add explanations outside the JSON.
"""
