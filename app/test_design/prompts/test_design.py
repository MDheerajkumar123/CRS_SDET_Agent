from textwrap import dedent


def build_test_design_prompt(
    document_name: str,
    requirement_context: str,
    risk_strategy_context: str,
    scenario_context: str,
) -> str:
    return dedent(
        f"""
        You are a Senior SDET and Test Design Engineer.

        Your task is to create a structured test design for the validated
        test scenarios derived from the customer requirement specification.

        DOCUMENT:
        {document_name}

        VALIDATED REQUIREMENTS:
        {requirement_context}

        VALIDATED RISK & TEST STRATEGY:
        {risk_strategy_context}

        VALIDATED TEST SCENARIOS:
        {scenario_context}

        OBJECTIVE:
        Convert validated test scenarios into detailed test-design items
        that will later be used by the Test Case Agent.

        TEST DESIGN RULES:

        1. Requirement Traceability
           - Every test design must reference a valid requirement_id.
           - Every test design must reference a valid scenario_id.
           - Do not create designs for requirements or scenarios that are
             not present in the supplied context.

        2. Source Fidelity
           - Use only information supported by the supplied requirements,
             risk strategy, and scenarios.
           - Do not invent business rules, workflows, APIs, databases,
             screens, integrations, values, limits, or implementation
             details.

        3. Test Design Techniques

          The field "test_design_technique" MUST contain exactly ONE of
          the following values:

          - Equivalence Partitioning
          - Boundary Value Analysis
          - Decision Table
          - State Transition
          - Error Guessing
          - Pairwise
          - Use Case

          These are the ONLY valid TestDesignTechnique values.

          NEVER use test types, scenario types, risk levels, requirement types,
          or other classifications as test_design_technique values.

          INVALID examples include:
          - Functional
          - Negative
          - Boundary
          - Integration
          - Regression
          - Security
          - Performance
          - Usability
          - Compatibility
          - Reliability
          - Auditability
          - Positive
          - High
          - Critical

          Important:
          - "Boundary" is a ScenarioType, but "Boundary Value Analysis" is
            a TestDesignTechnique.
          - "Performance", "Security", "Regression", "Integration", etc. are
            test/scenario categories, NOT design techniques.

        4. Risk Alignment
           - High and critical-risk scenarios must receive appropriate
             test-design depth.
           - Negative, boundary, error, integration, security,
             performance, usability, compatibility, and regression
             scenarios must be designed according to their nature.

        5. Test Data Conditions
           Define meaningful test-data conditions where supported.
           Do not invent exact values when the CRS does not specify them.

        6. Coverage
           Clearly identify what requirement/scenario behavior is covered.
           Avoid unnecessary duplication.

        7. Expected Focus
           Describe the behavior that the eventual test case should verify.
           Do not write a full test case with step-by-step execution yet.

        8. Separation From Test Cases
           This stage produces TEST DESIGN only.
           Do not generate:
           - detailed test steps
           - test execution instructions
           - actual automation code
           - Selenium/Playwright/API scripts
           - fabricated expected values

        9. Duplicate Avoidance
           Avoid creating multiple designs that test the same condition
           unless different techniques or risk areas genuinely require them.

        10. Confidence
            Provide an overall confidence score between 0 and 1 based on
            the quality and completeness of the source information.

        REQUIRED OUTPUT:

        Return ONLY valid JSON matching this structure:

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

        IMPORTANT:
        - Return valid JSON only.
        - Do not use Markdown code fences.
        - Do not add explanations outside the JSON.
        - Preserve traceability to the supplied source data.
        """
    ).strip()
