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

# Business Problem

Modern software teams often face **flaky tests** — tests that randomly pass or fail without any code changes.

These failures:
- Waste developer time
- Slow down CI/CD pipelines
- Reduce confidence in automated testing
- Make debugging difficult

The goal of this project is to automatically identify flaky tests and provide AI-generated explanations for their likely causes.

---

# Solution Overview

The system performs:

1. Historical test execution analysis
2. Flaky test detection
3. Failure log analysis
4. AI-powered root cause explanation
5. Recommended fix generation
6. Investigation report generation
7. Interactive dashboard visualization

---

# Features

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

# System Architecture

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

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Database | SQLite |
| AI Model | Ollama + Llama 3 |
| Data Processing | Pandas |
| ORM | SQLAlchemy |
| Testing | Pytest |
| Version Control | Git & GitHub |

## Project Structure

```text
Flaky_Test_Detector/
│
├── app.py
├── detector.py
├── explainer.py
├── agent.py
├── database.py
├── config.py
│
├── data/
│   ├── test_runs.csv
│   └── failure_logs.json
│
├── reports/
│   └── flaky_test_report.json
│
├── tests/
│   └── test_detector.py
│
├── prompts/
│   └── rootcause.txt
│
├── requirements.txt
└── README.md
```

## Installation

### Clone Repository
```bash
git clone <repository-url>
cd Flaky_Test_Detector
```

### Create Virtual Environment
```bash
python -m venv venv
```

### Activate Environment
**Windows:**
```powershell
venv\Scripts\activate
```
**Linux / Mac:**
```bash
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Run Streamlit Dashboard
```bash
streamlit run app.py
```

### Run Agent
```bash
python agent.py
```

### Run Detector
```bash
python detector.py
```

---

# Sample Data Folder

The `data/` folder contains sample datasets used for demonstration.

**`test_runs.csv`**
Contains:
- Test Name
- Status (PASS/FAIL)
- Duration
- Timestamp

**`failure_logs.json`**
Contains:
- Failure traces
- Error messages
- Timeout logs
- Infrastructure failures

---

# Test Cases

Pytest is used to validate the detection engine.

**Run:**
```bash
python -m pytest -v
```

**Covered Scenarios:**
- CSV Loading
- Missing File Handling
- Invalid Schema Validation
- Statistics Calculation
- Flaky Detection Logic
- Severity Classification
- Trend Analysis

---

# AI Usage Note

AI tools were actively used during development to accelerate implementation, architecture planning, debugging, testing, and documentation. See `AI_USAGE_NOTE.md` for a detailed breakdown.

**AI Tools Used:**
- ChatGPT
- Cursor AI
- Ollama (Llama 3)

**AI Assistance Areas:**
- Project architecture design
- Streamlit dashboard development
- Agent workflow implementation
- Database integration
- Unit test generation
- Documentation creation
- Root-cause analysis prompt engineering

---

# AI Capability Demonstrated

### Agent Loop
The autonomous agent:
- Loads execution data
- Detects flaky tests
- Reads failure logs
- Invokes LLM analysis
- Generates explanations
- Saves results
- Produces reports

### External Service Integration
The application integrates with:
- **Ollama Local AI Service**
- **Llama 3 Model**
For automated root-cause analysis and recommendation generation.

---

# Assumptions & Limitations

### Assumptions
- Historical test execution data is available in CSV format.
- Failure logs are provided in a structured JSON format.
- Ollama is installed and running locally on the deployment machine.
- The Llama 3 model has been pulled and is available via Ollama.

### Limitations
- Root-cause explanations are AI-generated and may require human validation.
- Detection accuracy depends heavily on the volume of available historical data.
- The current implementation focuses on proof-of-concept scale datasets and local execution.

---

# Future Enhancements

- CI/CD Integration
- Real-time Monitoring
- Multi-model Support
- Advanced Trend Forecasting
- Cloud Deployment
- Team Collaboration Features

---

# Conclusion

**Flaky Test Detector & Explainer** helps QA and development teams automatically identify unstable tests, understand probable root causes, and reduce debugging effort through AI-powered analysis and automation.
