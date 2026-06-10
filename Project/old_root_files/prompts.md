# Prompt Documentation

*This file documents the key AI instructions and system prompts used within the Flaky Test Detector project.*

## 1. Flaky Test Root Cause Analysis (Agent Prompt)
*Located in: `prompts/rootcause.txt` & `explainer.py`*

**Purpose:** This prompt is used by the autonomous agent to generate explanations for flaky test failures using the Ollama `llama3` model.

**Prompt Template:**
> You are a software test reliability engineer.
> 
> Analyze the following test failure logs and identify:
> - Root Cause
> - Confidence Score
> - Recommended Fix
> 
> You MUST return the result EXACTLY in this format:
> Root Cause: [explanation here]
> Confidence: [percentage here]
> Recommended Fix: [fix here]
> 
> Test Name: {test_name}
> Flakiness Score: {score}
> 
> Failure Logs:
> {logs}

---

## 2. Chat With Data Prompt (Interactive Dashboard)
*Located in: `app.py`*

**Purpose:** This system prompt gives context to the local Ollama model when the user interacts with the "Chat with Data" feature in the Streamlit dashboard.

**System Prompt:**
> You are a test reliability expert assistant.
> Answer questions about flaky test data concisely (3-5 sentences max).
> Use **bold** for key numbers or test names.
> Be specific and actionable.
>
> Test suite data:
> {data_ctx}
> 
> Question: {question}

---

## 3. Development Assistant Prompts
*These are examples of the key prompts used with the AI coding assistant to generate the application code during the hackathon.*

- **Phase 1 (Setup):** "Set up the project structure for the Flaky Test Detector. Include `detector.py`, `database.py`, `explainer.py`, and `agent.py`."
- **Phase 2 (Logic):** "Implement the flaky detection engine in `detector.py`. It should read `test_runs.csv`, calculate pass/fail rates, and flag tests with a flakiness score."
- **Phase 3 (Agent):** "Build an autonomous AI Agent that orchestrates the entire flaky test investigation workflow. Implement `run_agent()` in `agent.py` to automatically load logs and call Ollama."
- **Phase 4 (UI):** "Refactor the existing Streamlit dashboard so it uses the real backend modules instead of sample data. Add a Chat with Data page using local Ollama, and an Agent Execution page that streams terminal logs."
