import pandas as pd
import os
from typing import Tuple, Dict, List, Any

# Alias dictionaries
TEST_NAME_ALIASES = {'test_name', 'testcase', 'test_case', 'test', 'name', 'scenario'}
STATUS_ALIASES = {'status', 'result', 'outcome', 'state'}
DURATION_ALIASES = {'execution_time_ms', 'duration', 'runtime', 'execution_time', 'time_taken', 'time', 'duration_seconds'}
TIMESTAMP_ALIASES = {'timestamp', 'date', 'datetime', 'run_time', 'execution_date', 'run_date'}
RUN_ID_ALIASES = {'run_id', 'build_id', 'execution_id', 'run'}

def load_file(file_path: str) -> Tuple[pd.DataFrame, Dict[str, str], List[str]]:
    """
    Loads an arbitrary CSV, JSON, or Excel file and standardizes its schema.
    Returns: (DataFrame, mapping_dict, list_of_warnings)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext == '.json':
            df = pd.read_json(file_path)
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            # default to csv
            df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        raise ValueError("The provided file is empty.")
    except Exception as e:
        raise ValueError(f"Failed to read file {file_path}: {e}")

    if df.empty:
        raise ValueError("The provided file is empty.")

    return process_dataframe(df)

def process_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str], List[str]]:
    mapping = detect_schema(df)
    normalized_df = normalize_schema(df, mapping)
    final_df, warnings = validate_data(normalized_df)
    return final_df, mapping, warnings

def detect_schema(df: pd.DataFrame) -> Dict[str, str]:
    mapping = {}
    cols = list(df.columns)
    cols_lower = [str(c).lower().strip() for c in cols]
    
    # 1. Exact/Alias matching
    for orig_col, lower_col in zip(cols, cols_lower):
        if lower_col in TEST_NAME_ALIASES and 'test_name' not in mapping.values():
            mapping[orig_col] = 'test_name'
        elif lower_col in STATUS_ALIASES and 'status' not in mapping.values():
            mapping[orig_col] = 'status'
        elif lower_col in DURATION_ALIASES and 'duration' not in mapping.values():
            mapping[orig_col] = 'duration'
        elif lower_col in TIMESTAMP_ALIASES and 'timestamp' not in mapping.values():
            mapping[orig_col] = 'timestamp'
        elif lower_col in RUN_ID_ALIASES and 'run_id' not in mapping.values():
            mapping[orig_col] = 'run_id'

    # 2. Heuristic inference for missing ones
    mapped_vals = list(mapping.values())
    for orig_col, lower_col in zip(cols, cols_lower):
        if orig_col in mapping:
            continue
            
        sample_vals = df[orig_col].dropna().astype(str).str.lower().tolist()
        if not sample_vals:
            continue
            
        # Infer status
        if 'status' not in mapped_vals:
            if any(val in ['pass', 'fail', 'passed', 'failed', 'success', 'error', 'ok'] for val in sample_vals):
                mapping[orig_col] = 'status'
                mapped_vals.append('status')
                continue
                
        # Infer duration (check if numeric and values seem like ms/s)
        if 'duration' not in mapped_vals:
            if 'ms' in lower_col or 'second' in lower_col:
                mapping[orig_col] = 'duration'
                mapped_vals.append('duration')
                continue
            # Try numeric heuristics
            if pd.api.types.is_numeric_dtype(df[orig_col]):
                mapping[orig_col] = 'duration'
                mapped_vals.append('duration')
                continue
                
        # Infer test_name (often contains 'test' in values or is the first string column)
        if 'test_name' not in mapped_vals:
            if any('test' in str(val).lower() for val in sample_vals):
                mapping[orig_col] = 'test_name'
                mapped_vals.append('test_name')
                continue

    return mapping

def normalize_schema(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    df_new = df.copy()
    df_new.rename(columns=mapping, inplace=True)
    return df_new

def validate_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    warnings = []
    
    if 'test_name' not in df.columns:
        warnings.append("Test name column not found. Defaulting to first column or sequential names.")
        if not df.empty and len(df.columns) > 0 and 'status' not in df.columns[0] and 'duration' not in df.columns[0]:
             # Just use the first available unmapped column ideally, or first column.
             # For safety, just use first column as a fallback if not mapped.
             pass # Actually we just use first column below if nothing better.
             df['test_name'] = df.iloc[:, 0].astype(str)
        else:
            df['test_name'] = [f"Unknown_Test_{i}" for i in range(len(df))]
            
    if 'status' not in df.columns:
        warnings.append("Status column not found. Assuming all tests 'failed' for worst-case analysis.")
        df['status'] = 'failed'
        
    if 'duration' not in df.columns:
        warnings.append("Execution time column not found. Analysis will continue with reduced accuracy (duration=0).")
        df['duration'] = 0.0
        
    if 'timestamp' not in df.columns:
        warnings.append("Timestamp column not found. Generating default timestamps.")
        df['timestamp'] = pd.Timestamp.now()
        
    if 'run_id' not in df.columns:
        warnings.append("Run ID column not found. Creating sequential IDs.")
        df['run_id'] = range(1, len(df) + 1)
        
    # Normalize statuses
    df['status'] = df['status'].astype(str).str.lower()
    df['status'] = df['status'].apply(lambda x: 'passed' if 'pass' in x or 'success' in x or x == 'ok' else 'failed')
    
    # Ensure duration is numeric
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce').fillna(0.0)

    return df, warnings
