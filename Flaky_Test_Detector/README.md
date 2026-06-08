# Flaky Test Detector & Explainer

A hackathon project designed to analyze historical test execution data, detect flaky automated tests, and use an LLM (Large Language Model) to explain possible root causes of those failures.

## Problem Statement

Some automated tests pass sometimes and fail sometimes without any code changes. These are known as **flaky tests**. Flaky tests erode trust in automated test suites, delay releases, and waste engineering time. Identifying flaky tests manually and debugging their root causes is a tedious and time-consuming process.

## Proposed Solution

The **Flaky Test Detector & Explainer** solves this by:
1. **Detecting Flakiness**: Analyzing historical test runs to identify tests with inconsistent results (both passes and failures) for the same codebase state.
2. **Explaining Failures**: Leveraging local LLMs (via Ollama) with structured prompts to analyze failure log outputs, identify the likely root cause (e.g., race conditions, network timeout, database state), and recommend actionable fixes.
3. **Automated Orchestration**: Providing an intelligent agent loop to automatically scan, detect, explain, and store findings.

## Architecture Overview

The system is composed of the following components:
- **Frontend Dashboard (`app.py`)**: A Streamlit user interface to visualize flaky test statistics, view generated explanations, and trigger detection sweeps.
- **Detector Engine (`detector.py`)**: Responsible for loading and analyzing historical test runs to calculate flakiness metrics.
- **LLM Explainer (`explainer.py`)**: Interacts with the LLM via Ollama to generate root cause reports based on failure stack traces.
- **Agent Loop (`agent.py`)**: Coordinates the detector, database, and explainer to run scheduled or trigger-based scans.
- **Storage Layer (`database.py`)**: SQLite database backed by SQLAlchemy to store test run analysis history and LLM explanations.

## Folder Structure

```text
Flaky_Test_Detector/
│
├── app.py              # Streamlit Web Application
├── detector.py         # Flaky Test Detection Logic
├── explainer.py        # LLM Root Cause Explanation Logic
├── agent.py            # Agent Orchestration Loop
├── database.py         # SQLite & SQLAlchemy Database Layer
├── requirements.txt    # Python Project Dependencies
├── README.md           # Project Documentation
│
├── data/               # Raw Input Data Store
│   ├── test_runs.csv   # Historical test execution metadata
│   └── failure_logs.json # Error logs/stack traces for failed tests
│
├── prompts/            # LLM Prompt Templates
│   └── rootcause.txt   # Prompt structure for root cause analysis
│
├── reports/            # Generated Analysis Reports
│
├── tests/              # Automated Test Suite
│   └── test_detector.py
│
└── assets/             # Media and Static Assets
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai/) installed and running locally

### Installation

1. Navigate to the project root directory:
   ```bash
   cd Flaky_Test_Detector
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Launch the Streamlit dashboard:
   ```bash
   streamlit run app.py
   ```

## Future Enhancements

- **CI/CD Integration**: Automatically ingest test run artifacts from GitHub Actions, GitLab CI, or Jenkins.
- **Advanced Agent Behavior**: Implement auto-retries of flaky tests in isolated environments to capture dynamic state logs.
- **Model Fine-Tuning**: Optimize LLM prompt templates and configurations for specialized testing frameworks (e.g., Playwright, Selenium, Pytest).
