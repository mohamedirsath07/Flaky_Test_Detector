# Flaky Test Detector & Explainer

An AI-powered system that automatically detects flaky tests from historical test execution data, identifies instability patterns, and generates root-cause explanations with recommended fixes using a local LLM (Ollama + Llama 3).

---

## Team Information

### Team Name
**Team Syndicates**

### Team Members
- Mukkesh
- Mohamed Irsath
- Vigneshkumar
- Ragul

---

## Project Title

**Flaky Test Detector & Explainer**

---

## Live Demo

🔗 Live Demo: *To be added*

---

## Business Problem

Modern software teams often face **flaky tests** — tests that randomly pass or fail without any code changes.

These failures:
- Waste developer time
- Slow down CI/CD pipelines
- Reduce confidence in automated testing
- Make debugging difficult

The goal of this project is to automatically identify flaky tests and provide AI-generated explanations for their likely causes.

---

## Solution Overview

The system performs:

1. Historical test execution analysis
2. Flaky test detection
3. Failure log analysis
4. AI-powered root cause explanation
5. Recommended fix generation
6. Investigation report generation
7. Interactive dashboard visualization

---

## Features

### Flaky Test Detection
- Identifies tests with mixed pass/fail outcomes
- Calculates flakiness score
- Assigns severity levels

### AI Root Cause Analysis
- Uses Ollama + Llama 3
- Analyzes failure traces
- Generates:
  - Root Cause
  - Confidence Score
  - Recommended Fixes

### Autonomous Agent Workflow
- Loads test data
- Detects flaky tests
- Collects failure logs
- Generates explanations
- Saves results
- Creates reports

### Interactive Dashboard
- Upload CSV files
- View flaky tests
- Explore AI explanations
- Run investigations
- Download reports
- Chat with data

---

## System Architecture

```text
CSV / JSON Input
        │
        ▼
Detector Engine
        │
        ▼
Flaky Test Identification
        │
        ▼
Agent Workflow
        │
        ▼
Ollama (Llama 3)
        │
        ▼
Root Cause Analysis
        │
        ▼
SQLite Database
        │
        ▼
Streamlit Dashboard
        │
        ▼
Reports & Insights
```

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.ai/) installed locally with the `llama3` model pulled (`ollama run llama3`).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mukkesh16/Flaky_Test_Detector.git
   cd Flaky_Test_Detector
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

To launch the interactive dashboard, run:
```bash
streamlit run Flaky_Test_Detector/app.py
```
*(If you are running from the root directory on Windows, use `.\venv\Scripts\python.exe -m streamlit run Flaky_Test_Detector\app.py`)*

---

## Tech Stack
- **Frontend:** Streamlit
- **Backend Core:** Python 3
- **Data Processing:** Pandas
- **Database:** SQLite & SQLAlchemy
- **AI/LLM:** Ollama (Llama 3)
