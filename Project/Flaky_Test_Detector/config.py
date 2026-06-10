"""
config.py
Centralized configuration settings for the Flaky Test Detector project.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
TEST_RUNS_CSV = os.path.join(BASE_DIR, "data", "test_runs.csv")
FAILURE_LOGS_JSON = os.path.join(BASE_DIR, "data", "failure_logs.json")
REPORT_PATH = os.path.join(BASE_DIR, "reports", "flaky_test_report.json")

# Database configuration
DATABASE_NAME = "results.db"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}"

# Ollama model configuration
OLLAMA_MODEL = "llama3"

# Groq Cloud configuration (Fallback)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", None)
GROQ_MODEL = "llama-3.1-8b-instant"
