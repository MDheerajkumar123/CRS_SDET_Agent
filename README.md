# QAGenesis

## AI-Powered Requirement-to-Test Engineering

QAGenesis is a multi-agent AI-powered SDET/QA system that transforms a Customer Requirement Specification (CRS) into structured, traceable QA artifacts.

The project explores how Generative AI, Retrieval-Augmented Generation (RAG), multi-agent orchestration, validation, and rework loops can be combined to support the software testing lifecycle.

---

## 🎯 Project Objective

The objective of QAGenesis is to automate the transformation of requirements into structured QA artifacts while maintaining:

- Requirement traceability
- Source fidelity
- Structured outputs
- Risk-based test coverage
- Test design consistency
- Validation of AI-generated artifacts
- Reviewer-driven rework
- Requirements Traceability Matrix (RTM) coverage

QAGenesis does not simply generate test cases from a prompt.

Each major artifact can be reviewed and validated before the workflow proceeds.

---

## 🔄 End-to-End Workflow

    Customer Requirement Specification
                  │
                  ▼
           CRS Ingestion
                  │
                  ▼
        Requirement Analyzer
                  │
                  ▼
       Requirement Validator
                  │
                  ▼
        Risk & Test Strategy
                  │
                  ▼
         Scenario Generator
                  │
                  ▼
          Scenario Validator
                  │
                  ▼
             Test Design
                  │
                  ▼
        Test Case Generator
                  │
                  ▼
        Test Case Validator
                  │
                  ▼
             RTM Generator
                  │
                  ▼
             RTM Validator
                  │
                  ▼
           Final QA Reviewer
                  │
                  ▼
            Excel Generator
                  │
                  ▼
           Final QA Package

### UI Workflow

The Streamlit dashboard exposes the main workflow as 12 visible stages:

1. Requirement Analyzer
2. Requirement Validator
3. Risk & Test Strategy
4. Scenario Generator
5. Scenario Validator
6. Test Design
7. Test Case Generator
8. Test Case Validator
9. RTM Generator
10. RTM Validator
11. Final QA Reviewer
12. Excel Generator

CRS ingestion is handled internally by the workflow.

---

## 🤖 Multi-Agent Validation Architecture

One of the key design principles of QAGenesis is that generated artifacts should not automatically be accepted.

The workflow uses a generator/reviewer approach:

    Working Agent
          │
          ▼
       Reviewer
          │
     ┌────┴────┐
     │         │
    PASS     REWORK
     │         │
     ▼         ▼
 Next Stage  Feedback
               │
               ▼
             Rework
               │
               ▼
            Reviewer

This approach is used to identify issues such as:

- Missing requirement coverage
- Invalid traceability
- Missing scenarios
- Incorrect classifications
- Unsupported assumptions
- Hallucinated implementation details
- Test case quality problems
- RTM coverage gaps

The validation loops support configurable retry/rework behavior.

---

## 🧠 RAG-Based Requirement Processing

QAGenesis uses a retrieval-based approach for working with CRS content.

    CRS Document
         │
         ▼
    Document Parser
         │
         ▼
       Cleaning
         │
         ▼
      Chunking
         │
         ▼
      Embeddings
         │
         ▼
       ChromaDB
         │
         ▼
 Relevant CRS Context
         │
         ▼
      AI Agents

Supported document ingestion includes:

- DOCX
- PDF
- TXT

The retrieved CRS context is supplied to the relevant analysis stage instead of relying only on the complete document being repeatedly passed to every agent.

---

## 🧩 QA Artifacts Generated

QAGenesis generates structured artifacts throughout the workflow.

### Requirements

Extracts and classifies testable requirements from the CRS.

### Risk & Test Strategy

Identifies risks and associates appropriate testing strategies with the requirements.

### Test Scenarios

Generates scenarios covering applicable areas such as:

- Positive
- Negative
- Boundary
- Error
- Integration
- Security
- Performance
- Reliability
- Usability
- Compatibility
- Regression

### Test Design

Applies defined test design techniques including:

- Equivalence Partitioning
- Boundary Value Analysis
- Decision Table
- State Transition
- Error Guessing
- Pairwise
- Use Case

### Test Cases

Generates structured test cases containing:

- Test Case ID
- Design ID
- Scenario ID
- Requirement ID
- Title
- Objective
- Test Type
- Priority
- Preconditions
- Test Data
- Steps
- Expected Results
- Source Design

### Requirements Traceability Matrix

Creates an RTM connecting:

    Requirement
         ↓
      Scenario
         ↓
     Test Design
         ↓
      Test Case

---

## 🛡️ Source Fidelity & Hallucination Controls

A major focus of the project is preventing AI agents from introducing unsupported technical details.

For example, if the CRS does not define an implementation technology, the test case generator should not invent:

- HTTP status codes
- REST endpoints
- Authentication tokens
- JWT
- API keys
- Database implementation details
- SQL
- Specific infrastructure
- Unsupported performance targets
- Unsupported monitoring metrics
- Technology-specific implementation assumptions

The Test Case Generator performs source-fidelity checks before producing the structured output.

The successful V1 validation run confirmed that the generated QA package contained no unsupported assumptions identified by the Final QA Reviewer.

---

## 🔌 LLM Provider Architecture

QAGenesis supports multiple LLM providers through a centralized LLM manager.

Current providers include:

- Google Gemini
- Groq
- OpenRouter

Different workflow tasks can be routed to different providers.

    LLM Manager
         │
    ┌────┼────┐
    ▼    ▼    ▼
 Gemini Groq OpenRouter
    │    │    │
    └────┼────┘
         │
    QA Workflow

The LLM manager also supports provider fallback handling when a configured provider fails.

This allows the workflow to attempt another configured provider rather than immediately terminating the entire workflow.

---

## 🖥️ Streamlit Dashboard

QAGenesis includes a Streamlit-based UI for running and observing the workflow.

The dashboard provides:

- CRS upload
- Analysis configuration
- Workflow execution
- Live workflow stages
- Agent execution status
- Provider/model information
- Workflow logs
- QA metrics
- Final validation results
- Excel output/download

The UI uses workflow events to display the progress of the actual workflow rather than relying on simulated progress timers.

---

## 📊 V1 Validation

The current V1 implementation has been executed through the complete workflow using a CRS validation document.

### Final QA Result

    Status: PASS
    Score: 95 / 100
    Retries: 0
    Issues: 0
    Required Changes: 0

### RTM Result

    Requirement Coverage: 100%

The final Excel package contains structured sheets for:

- Summary
- Requirements
- Risk Strategy
- Scenarios
- Test Designs
- Test Cases
- RTM

The successful validation run demonstrated complete traceability across the generated QA artifacts.

---

## 🛠️ Technology Stack

| Area | Technology |
|---|---|
| Language | Python |
| Agent Framework | CrewAI |
| LLM Providers | Gemini, Groq, OpenRouter |
| RAG / Vector Store | ChromaDB |
| Data Validation | Pydantic |
| UI | Streamlit |
| Document Processing | python-docx, pypdf |
| Excel Generation | OpenPyXL |
| Testing | Pytest |
| Environment | Windows / VS Code |

---

## 📁 Project Structure

    CRS_SDET_Agent/
    │
    ├── app/
    │   ├── ingestion/
    │   ├── llm/
    │   ├── observability/
    │   ├── orchestrator/
    │   ├── requirement/
    │   ├── risk/
    │   ├── scenario/
    │   ├── test_design/
    │   ├── test_case/
    │   ├── rtm/
    │   ├── final_review/
    │   └── validation/
    │
    ├── data/
    │   └── input/
    │
    ├── output/
    │
    ├── tests/
    │   ├── ui/
    │   └── ...
    │
    ├── ui/
    │   ├── components/
    │   ├── services/
    │   ├── state/
    │   └── streamlit_app.py
    │
    ├── .env.example
    ├── .gitignore
    ├── requirements.txt
    └── README.md

---

## ⚙️ Installation

### 1. Clone the repository

    git clone https://github.com/MDheerajkumar123/CRS_SDET_Agent.git
    cd CRS_SDET_Agent

### 2. Create a virtual environment

Python 3.12 is recommended for the current project environment.

#### Windows

    python -m venv .venv

Activate it:

    .venv\Scripts\Activate.ps1

### 3. Install dependencies

    pip install -r requirements.txt

---

## 🔐 Environment Configuration

Create a `.env` file based on `.env.example`.

Example:

    GEMINI_API_KEY=your_gemini_api_key
    GROQ_API_KEY=your_groq_api_key
    OPENROUTER_API_KEY=your_openrouter_api_key

    GEMINI_MODEL=your_gemini_model
    GROQ_MODEL=your_groq_model
    OPENROUTER_MODEL=your_openrouter_model

API keys should never be committed to GitHub.

---

## ▶️ Running the Application

From the project root:

    streamlit run ui/streamlit_app.py

The Streamlit application will open in the browser.

Upload a CRS document and configure the analysis before starting the workflow.

---

## 🧪 Running Tests

The project uses Pytest.

Run the complete test suite:

    pytest -q

Individual areas can also be tested separately.

For example:

    pytest -q tests/test_test_case_generation_prompt.py

---

## 📤 Output

The workflow produces an Excel QA package containing structured artifacts.

Typical output:

    output/
    └── CRS_SDET_Final_Output.xlsx

The workbook contains:

    Summary
    Requirements
    Risk Strategy
    Scenarios
    Test Designs
    Test Cases
    RTM

---

## 🚫 V1 Scope

QAGenesis V1 focuses on QA artifact generation and validation.

The following are outside the current V1 scope:

- Actual test execution
- Selenium/Playwright execution
- API test execution
- CI/CD execution
- Jira defect creation
- Production monitoring
- Database execution
- Actual performance/load execution
- Actual security test execution

The system may design test cases for these areas when supported by the CRS, but V1 does not execute those tests against a live system.

---

## 🔭 Future Improvements

Potential future development areas include:

- Improved agent observability
- More detailed workflow analytics
- Additional document formats
- Expanded test design capabilities
- Improved rework strategies
- Additional LLM providers
- Persistent workflow history
- Multiple CRS/project management
- Advanced QA metrics
- Integration with test management platforms
- Integration with issue tracking systems
- API and browser automation execution

---

## 📌 Project Status

**Current Status: V1 Completed and Validated**

Current V1 validation:

    End-to-End Workflow       ✅
    Multi-Agent Architecture  ✅
    Validation/Rework Loops   ✅
    RAG / ChromaDB            ✅
    LLM Provider Fallback     ✅
    Streamlit UI              ✅
    Final QA Review           ✅ 95/100
    RTM Coverage              ✅ 100%
    Excel Output              ✅

---

## 👨‍💻 Author

**Dheeraj Kumar**

AI / QA / SDET Engineering Project

---

## ⭐ Project Focus

QAGenesis explores the intersection of:

    Software Testing
           +
    SDET Engineering
           +
    Generative AI
           +
    RAG
           +
    Multi-Agent Systems
           +
    LLM Orchestration
           +
    Quality Engineering

The objective is not to replace QA engineering, but to explore how AI agents can assist in transforming requirements into structured, reviewable, and traceable QA artifacts.

---

## 🔗 Repository

GitHub: https://github.com/MDheerajkumar123/CRS_SDET_Agent
