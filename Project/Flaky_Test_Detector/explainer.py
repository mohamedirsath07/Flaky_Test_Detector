"""
explainer.py - AI Root Cause Explainer Module

Uses the local Ollama LLM (llama3) to analyze flaky test failures
and return structured root cause analysis.
"""

import os
import logging
import re
from typing import Optional

import requests
import ollama
from config import GROQ_API_KEY, GROQ_MODEL

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _load_prompt_template() -> Optional[str]:
    """
    Loads the prompt template from prompts/rootcause.txt.

    Returns:
        Optional[str]: The prompt template string, or None if not found.
    """
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "rootcause.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Prompt template not found: {prompt_path}")
        return None


def _build_prompt(template: str, test_name: str, score: float, logs: list[str]) -> str:
    """
    Builds the final prompt by replacing placeholders in the template.

    Args:
        template (str): The raw prompt template with placeholders.
        test_name (str): Name of the flaky test.
        score (float): Flakiness score.
        logs (list[str]): List of failure log strings.

    Returns:
        str: The fully formatted prompt string.
    """
    formatted_logs = "\n".join(logs)
    return template.format(test_name=test_name, score=score, logs=formatted_logs)


def _parse_llm_response(content: str) -> Optional[dict]:
    """
    Parses the LLM response text to extract structured fields.

    Expects the model output to contain:
      Root Cause: ...
      Confidence: ...
      Recommended Fix: ...

    Args:
        content (str): Raw text response from the LLM.

    Returns:
        Optional[dict]: Parsed fields or None if parsing fails.
    """
    root_cause_match = re.search(
        r"(?:Root Cause|Likely Root Cause)[\s:]*(.+?)(?=(?:Confidence|Recommended Fix)[\s:]|$)",
        content, re.DOTALL | re.IGNORECASE
    )
    confidence_match = re.search(
        r"Confidence(?:\s*Percentage)?[\s:]*(.+?)(?=(?:Root Cause|Likely Root Cause|Recommended Fix)[\s:]|$)",
        content, re.DOTALL | re.IGNORECASE
    )
    fix_match = re.search(
        r"Recommended Fix[\s:]*(.+?)(?=(?:Root Cause|Likely Root Cause|Confidence)[\s:]|$)",
        content, re.DOTALL | re.IGNORECASE
    )

    if not (root_cause_match and confidence_match and fix_match):
        return None

    return {
        "root_cause": root_cause_match.group(1).strip(),
        "confidence": confidence_match.group(1).strip(),
        "recommended_fix": fix_match.group(1).strip(),
    }


def generate_explanation(test_name: str, score: float, logs: list[str]) -> dict:
    """
    Generates an AI-powered root cause explanation for a flaky test.

    Loads the prompt template, fills in the test details, sends the prompt
    to the local Ollama llama3 model, and parses the structured response.

    Args:
        test_name (str): The name of the flaky test.
        score (float): The calculated flakiness score (0.0 - 1.0).
        logs (list[str]): Failure log lines for the test.

    Returns:
        dict: A dictionary with keys:
            - test_name, root_cause, confidence, recommended_fix  (on success)
            - error  (on failure)
    """
    logger.info(f"Generating explanation for {test_name}")

    # Step 1: Load prompt template
    template = _load_prompt_template()
    if template is None:
        return {"error": "Prompt template not found."}

    # Step 2: Build prompt
    prompt = _build_prompt(template, test_name, score, logs)

    # Step 3: Call Ollama
    try:
        response = ollama.chat(model="llama3", messages=[
            {"role": "user", "content": prompt}
        ])
        logger.info("Ollama response received")
        content = response["message"]["content"]
    except Exception as e:
        logger.warning(f"Ollama failed ({e}). Falling back to Groq API...")
        if not GROQ_API_KEY:
            return {"error": "Ollama failed and GROQ_API_KEY is not set. Please set it or start Ollama."}
            
        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            }
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
            res.raise_for_status()
            content = res.json()["choices"][0]["message"]["content"]
            logger.info("Groq API response received")
        except Exception as groq_e:
            logger.error(f"Groq fallback failed: {groq_e}")
            return {"error": f"Both Ollama and Groq failed. Groq error: {groq_e}"}

    # Step 4: Parse response
    parsed = _parse_llm_response(content)
    if parsed is None:
        logger.error("Invalid response format from Ollama.")
        return {"error": "Invalid response format received from model.", "raw_response": content}

    return {
        "test_name": test_name,
        "root_cause": parsed["root_cause"],
        "confidence": parsed["confidence"],
        "recommended_fix": parsed["recommended_fix"],
    }


if __name__ == "__main__":
    # Standalone test mode
    sample_result = generate_explanation(
        test_name="login_test",
        score=0.33,
        logs=["Timeout waiting for element", "Connection reset"],
    )

    print("\n=================================")
    print("AI ROOT CAUSE ANALYSIS")
    print("=================================\n")

    if "error" in sample_result:
        print(f"Error: {sample_result['error']}")
    else:
        print(f"Test:\n{sample_result['test_name']}\n")
        print(f"Root Cause:\n{sample_result['root_cause']}\n")
        print(f"Confidence:\n{sample_result['confidence']}\n")
        print(f"Recommended Fix:\n{sample_result['recommended_fix']}")

    print("\n=================================")
