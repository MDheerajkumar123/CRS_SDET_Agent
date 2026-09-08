
from textwrap import dedent


def build_test_design_rework_prompt(
    document_name: str,
    requirement_context: str,
    risk_strategy_context: str,
    scenario_context: str,
    current_design_context: str,
    issues: list[str],
    required_changes: list[str],
    retry_count: int = 0,
) -> str:
    issues_text = "\n".join(
        f"- {issue}" for issue in issues
    ) or "- No specific issues supplied."

    changes_text = "\n".join(
        f"- {change}" for change in required_changes
    ) or "- No specific required changes supplied."

    return dedent(
        f"""
        You are a Senior SDET and Test Design Engineer performing
        controlled rework of an existing test-design artifact.

        DOCUMENT:
        {document_name}

        RETRY COUNT:
        {retry_count}

        VALIDATED REQUIREMENTS:
        {requirement_context}

        VALIDATED RISK & TEST STRATEGY:
        {risk_strategy_context}

        VALIDATED TEST SCENARIOS:
        {scenario_context}

        CURRENT TEST DESIGN:
        {current_design_context}

        FINAL QA REVIEW ISSUES:
        {issues_text}

        REQUIRED CHANGES:
        {changes_text}

        OBJECTIVE:
        Correct the identified problems in the current TestDesignAnalysis
        while preserving valid existing designs, traceability, coverage,
        techniques, and source fidelity.

        IMPORTANT RULES:

        1. REQUIREMENT TRACEABILITY
           - Every test design must reference an existing requirement_id
             from the supplied validated requirements.
           - Never invent requirement IDs.

        2. SCENARIO TRACEABILITY
           - Every test design must reference an existing scenario_id
             from the supplied validated scenarios.
           - Never invent scenario IDs.
           - source_scenario must correspond to the supplied scenario_id.

        3. SOURCE FIDELITY
           - Use only information supported by the supplied requirements,
             risk strategy, and scenarios.
           - Do not invent business rules, workflows, APIs, databases,
             screens, integrations, values, limits, or implementation
             details.

        4. TEST DESIGN TECHNIQUES
           Use only:
           - Equivalence Partitioning
           - Boundary Value Analysis
           - Decision Table
           - State Transition
           - Error Guessing
           - Pairwise
           - Use Case

           Select the technique appropriate to the supplied scenario.

        5. RISK ALIGNMENT
           - High and Critical risk areas require appropriate test-design
             depth.
           - Match the design to the scenario type and risk context.
           - Do not assign techniques merely to increase coverage.

        6. TEST DATA CONDITIONS
           - Define meaningful conditions only when supported by source data.
           - Do not invent exact values, limits, ranges, credentials,
             transaction amounts, or system configurations.

        7. COVERAGE
           - Clearly identify the requirement/scenario behavior covered.
           - Avoid unnecessary duplication.
           - Preserve valid existing coverage.

        8. EXPECTED FOCUS
           - Describe what the eventual test case should verify.
           - Do not generate detailed execution steps.
           - Do not generate automation code.

        9. PRESERVE VALID INFORMATION
           - Do not rewrite unaffected designs unnecessarily.
           - Preserve valid design IDs where possible.
           - Correct identified issues without damaging valid traceability.

        10. DUPLICATE AVOIDANCE
            Avoid multiple designs testing the same condition unless a
            genuinely different technique, risk area, or scenario justifies it.

        11. NO HALLUCINATION
            - Do not invent requirements.
            - Do not invent scenarios.
            - Do not invent business rules.
            - Do not invent implementation details.
            - Do not fabricate expected values.

        12. CONFIDENCE
            overall_design_confidence must be between 0 and 1.
            Lower confidence when source information is incomplete or
            ambiguous.

        13. SCOPE
            Rework only the Test Design artifact.
            Do not generate:
            - test cases
            - RTM
            - execution results
            - automation scripts
            - Selenium/Playwright/API code

        14. REVIEW ALIGNMENT
            Address the supplied Final QA issues and required changes.
            Do not introduce unrelated changes.

        OUTPUT REQUIREMENT:

        Return ONLY valid JSON matching the TestDesignAnalysis schema.

        Do not return:
        - Markdown
        - Code fences
        - Explanations outside JSON
        - Comments
        - Additional fields

        Expected structure:

        {{
          "document_name": "string",
          "design_summary": "string",
          "test_designs": [
            {{
              "design_id": "TD-001",
              "scenario_id": "SCN-001",
              "requirement_id": "REQ-001",
              "title": "string",
              "objective": "string",
              "test_design_technique": "Equivalence Partitioning",
              "test_data_conditions": [
                "string"
              ],
              "coverage_area": "string",
              "expected_focus": "string",
              "source_scenario": "SCN-001"
            }}
          ],
          "overall_design_confidence": 0.0
        }}
        """
    ).strip()
