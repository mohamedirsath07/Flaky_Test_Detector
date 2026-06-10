import os
import sys
import pandas as pd
import pytest

# Ensure the parent directory is in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parsers.universal_parser import load_file, detect_schema, validate_data

@pytest.fixture
def tmp_csv_path(tmp_path):
    def _create_csv(data_dict, filename="test.csv"):
        df = pd.DataFrame(data_dict)
        filepath = tmp_path / filename
        df.to_csv(filepath, index=False)
        return str(filepath)
    return _create_csv

@pytest.fixture
def tmp_json_path(tmp_path):
    def _create_json(data_dict, filename="test.json"):
        df = pd.DataFrame(data_dict)
        filepath = tmp_path / filename
        df.to_json(filepath, orient="records")
        return str(filepath)
    return _create_json

@pytest.fixture
def tmp_excel_path(tmp_path):
    def _create_excel(data_dict, filename="test.xlsx"):
        df = pd.DataFrame(data_dict)
        filepath = tmp_path / filename
        df.to_excel(filepath, index=False)
        return str(filepath)
    return _create_excel

def test_original_sample_format(tmp_csv_path):
    path = tmp_csv_path({
        "test_name": ["test_A", "test_B"],
        "status": ["pass", "fail"],
        "duration_seconds": [1.2, 0.5],
        "run_date": ["2026-06-01", "2026-06-02"]
    })
    
    df, mapping, warnings = load_file(path)
    
    assert "test_name" in df.columns
    assert "status" in df.columns
    assert "duration" in df.columns
    assert "timestamp" in df.columns
    
    # Should automatically normalize status to 'passed' or 'failed'
    assert df.iloc[0]["status"] == "passed"
    assert df.iloc[1]["status"] == "failed"

def test_jenkins_report_format(tmp_csv_path):
    path = tmp_csv_path({
        "testcase": ["LoginFeature", "SignupFeature"],
        "result": ["success", "error"],
        "execution_time_ms": [1200, 500]
    })
    
    df, mapping, warnings = load_file(path)
    
    assert df.iloc[0]["test_name"] == "LoginFeature"
    assert df.iloc[0]["status"] == "passed"
    assert df.iloc[0]["duration"] == 1200
    assert "Timestamp column not found" in warnings[0]

def test_github_actions_format(tmp_json_path):
    path = tmp_json_path({
        "name": ["action_test_1"],
        "outcome": ["success"],
        "runtime": [1.5],
        "datetime": ["2026-06-10T10:00:00Z"]
    })
    
    df, mapping, warnings = load_file(path)
    
    assert df.iloc[0]["test_name"] == "action_test_1"
    assert df.iloc[0]["status"] == "passed"
    assert df.iloc[0]["duration"] == 1.5

def test_excel_spreadsheet(tmp_excel_path):
    path = tmp_excel_path({
        "Scenario": ["E2E_Flow"],
        "State": ["Fail"],
        "Time_Taken": [4.5]
    })
    
    df, mapping, warnings = load_file(path)
    
    assert df.iloc[0]["test_name"] == "E2E_Flow"
    assert df.iloc[0]["status"] == "failed"
    assert df.iloc[0]["duration"] == 4.5

def test_missing_columns_graceful_handling(tmp_csv_path):
    path = tmp_csv_path({
        "random_col": ["val1"]
    })
    
    df, mapping, warnings = load_file(path)
    
    assert len(warnings) >= 4  # Should warn about name, status, duration, timestamp missing
    assert df.iloc[0]["test_name"] == "val1"
    assert df.iloc[0]["status"] == "failed"
    assert df.iloc[0]["duration"] == 0.0

def test_ai_heuristics_inference(tmp_csv_path):
    # Testing that it can infer status from values even if column name is completely obscure
    path = tmp_csv_path({
        "alpha": ["e2e_login_test", "api_auth_test"],  # should be inferred as test_name
        "beta": ["pass", "fail"],                    # should be inferred as status
        "gamma": [1.2, 0.5]                          # should be inferred as duration
    })
    
    df, mapping, warnings = load_file(path)
    
    assert df.iloc[0]["test_name"] == "e2e_login_test"
    assert df.iloc[0]["status"] == "passed"
    assert df.iloc[0]["duration"] == 1.2
    
def test_empty_file(tmp_path):
    filepath = tmp_path / "empty.csv"
    filepath.touch()
    
    with pytest.raises(ValueError, match="The provided file is empty"):
        load_file(str(filepath))
