# AI Usage Note

This document summarizes how Artificial Intelligence tools were utilized during the development of the **Flaky Test Detector & Explainer** project, in accordance with the hackathon submission guidelines.

## AI Tools Used
- **ChatGPT**
- **Claude**
- **Gemini**
- **Ollama (Local Llama 3)**

---

## 1. What AI Helped With
AI was actively utilized throughout the software development lifecycle to accelerate implementation and enhance the final product. Key areas of assistance included:

- **Project Architecture Design**: Structuring the application cleanly into modular components (`detector`, `explainer`, `agent`, `database`, `app`).
- **Streamlit Dashboard Development**: Rapidly prototyping the UI layout, metrics cards, and interactive dashboard components.
- **Agent Workflow Implementation**: Designing the orchestration loop to seamlessly connect flaky test detection with AI-driven explanations.
- **Database Integration**: Setting up robust SQLAlchemy models and SQLite connection management logic.
- **Unit Test Generation**: Creating comprehensive `pytest` test cases, including fixtures, edge cases (missing files, invalid schemas), and logic verifications to achieve a 100% pass rate.
- **Universal Parser Engine**: Refactoring strict CSV ingestion into a flexible, schema-agnostic mapping engine that infers missing columns using data heuristics.
- **API Fallbacks**: Implementing a seamless failover mechanism between local Ollama and the external Groq Cloud API for maximum reliability.
- **Documentation**: Structuring and formatting professional markdown files (like the `README.md`).
- **Prompt Engineering**: Refining the instructional prompts sent to the local LLM to ensure structured and accurate root-cause analysis outputs.

---

## 2. What AI Got Wrong
While highly beneficial, AI tools occasionally required manual correction and developer oversight:

- **Dependency and Syntax Hallucinations**: Occasionally suggested deprecated API calls or incompatible library versions in the `requirements.txt` that had to be manually resolved.
- **Simplistic Test Assertions**: Initial generations of unit tests sometimes included trivial assertions that did not effectively test the core business logic, necessitating manual refinement to achieve rigorous coverage.
- **LLM Output Formatting**: During early stages of prompt engineering, the local LLM sometimes hallucinated root causes not present in the failure logs or failed to adhere strictly to the requested response format, requiring iterative adjustments to the system prompt.

---

## 3. Best Prompts Used
The following prompts yielded the most effective and high-quality outputs during development:

**For System Architecture & Boilerplate Generation:**
> *"You are a Senior Python Software Engineer. I am building a hackathon project called 'Flaky Test Detector & Explainer'. The goal is to analyze test execution history, detect flaky tests, and use a local LLM to explain root causes. Please generate the complete project folder structure and architecture overview using best practices."*

**For Comprehensive Pytest Generation:**
> *"Write a comprehensive `pytest` test suite for the `detector.py` module. Include fixtures for temporary CSV files and in-memory pandas DataFrames. Ensure you test successful execution, missing files, empty files, invalid schemas, statistics calculation, flakiness detection logic, and severity classification. Target a 100% pass rate."*

**For LLM Root-Cause Analysis (System Prompt):**
> *"You are a senior QA engineer. Analyze the following flaky test.*
> *Test Name: {test_name}*
> *Flakiness Score: {score}*
> *Failure Logs: {logs}*
> *Provide:*
> *1. Likely Root Cause*
> *2. Confidence Percentage*
> *3. Recommended Fix"*
