"""
app.py
Flaky Test Detector & Explainer Dashboard
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import json
import os
import sys
import subprocess
from datetime import datetime
from ollama import Client

from config import OLLAMA_MODEL, TEST_RUNS_CSV, REPORT_PATH
from ui_components import (
    inject_global_css, render_topbar, render_sidebar,
    section_header, metric_row, score_badge,
    upload_card, callout, ai_explanation_card,
    chat_bubble, empty_state,
    PRIMARY, ACCENT, WARN, DANGER, BG_CARD, BG_LIGHT, TEXT_MAIN, TEXT_MUTED
)

# Backend Modules
from detector import load_test_runs, calculate_test_statistics, detect_flaky_tests
from database import initialize_database, get_all_results

st.set_page_config(
    page_title="FlakyDetect · Local AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session State ────────────────────────────────────────────────────────────
for k, v in {"df": None, "flaky_results": None, "chat_history": []}.items():
    if k not in st.session_state:
        st.session_state[k] = v

inject_global_css()
page = render_sidebar()

# ── Helper Functions ────────────────────────────────────────────────────────
def compute_stats(df):
    if "flakiness_score" not in df.columns:
        return {"total": len(df), "high_flaky": 0, "med_flaky": 0, "low_flaky": 0, "avg_score": 0.0, "worst_test": "None"}
    return {
        "total": len(df),
        "high_flaky": int((df["flakiness_score"] >= 0.75).sum()),
        "med_flaky": int(((df["flakiness_score"] >= 0.40) & (df["flakiness_score"] < 0.75)).sum()),
        "low_flaky": int((df["flakiness_score"] < 0.40).sum()),
        "avg_score": float(df["flakiness_score"].mean()),
        "worst_test": df.loc[df["flakiness_score"].idxmax(), "test_name"] if not df.empty else "None",
    }

def ollama_chat(messages: list) -> str:
    client = Client(host='http://127.0.0.1:11434')
    try:
        response = client.chat(model=OLLAMA_MODEL, messages=messages)
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

def answer_question_with_ai(question: str, df, history: list) -> str:
    """Stream-style Local Ollama answer about the dataframe."""
    data_ctx = "No data loaded yet."
    
    if df is not None:
        if isinstance(df, list):
            df = pd.DataFrame(df)
            
        if isinstance(df, pd.DataFrame) and not df.empty:
            if len(df) <= 20:
                data_ctx = df.to_markdown(index=False)
            else:
                try:
                    data_ctx = (
                        f"Columns: {list(df.columns)}\n"
                        f"Shape: {df.shape}\n"
                        f"Top 10 by flakiness:\n{df.nlargest(10,'flakiness_score').to_markdown(index=False)}\n"
                    )
                except Exception as e:
                    data_ctx = f"Data available, but couldn't format overview: {e}"

    system = (
        "You are a test reliability expert assistant. "
        "Answer questions about flaky test data concisely (3-5 sentences max). "
        "Use **bold** for key numbers or test names. "
        "Be specific and actionable."
    )

    messages = [{"role": "system", "content": system}]
    for turn in history[-4:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    
    messages.append({
        "role": "user",
        "content": f"Test suite data:\n{data_ctx}\n\nQuestion: {question}"
    })

    return ollama_chat(messages)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — UPLOAD
# ════════════════════════════════════════════════════════════════════════════

def page_upload():
    render_topbar("01 · Upload Data")
    section_header("📂", "Upload Test Data", "Load real test runs for the backend to process")

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        csv_file = upload_card("CSV Test Results", "CSV", "📄", ["csv"])
        if csv_file:
            try:
                # Save to the central data directory for the agent to pick up
                os.makedirs(os.path.dirname(TEST_RUNS_CSV), exist_ok=True)
                with open(TEST_RUNS_CSV, "wb") as f:
                    f.write(csv_file.getbuffer())
                
                # Load using real detector
                df = load_test_runs(TEST_RUNS_CSV)
                df = calculate_test_statistics(df)
                
                st.session_state.df = df
                st.session_state.flaky_results = detect_flaky_tests(df)
                callout(f"Loaded and processed <b>{len(df)}</b> records using detector.py", "success")
            except Exception as e:
                callout(f"Failed to process CSV: {e}", "error")

    with col_b:
        # Check if local data exists
        if os.path.exists(TEST_RUNS_CSV):
            st.markdown(f"<div style='margin-top:10px;text-align:center;'><p style='color:{TEXT_MUTED};'>Existing test_runs.csv detected.</p></div>", unsafe_allow_html=True)
            if st.button("Load Existing Local Data", use_container_width=True):
                try:
                    df = load_test_runs(TEST_RUNS_CSV)
                    df = calculate_test_statistics(df)
                    st.session_state.df = df
                    st.session_state.flaky_results = detect_flaky_tests(df)
                    callout("Loaded local data from data/test_runs.csv", "success")
                except Exception as e:
                    callout(f"Failed to load: {e}", "error")

    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown("<br>", unsafe_allow_html=True)
        section_header("📊", "Processed Dataset", f"{len(df)} tests analyzed by detector.py")
        st.dataframe(df, use_container_width=True, height=260)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — DETECTION RESULTS
# ════════════════════════════════════════════════════════════════════════════

def page_table():
    render_topbar("02 · Detection Results")

    if st.session_state.df is None or st.session_state.flaky_results is None:
        empty_state("📊", "No Data Available", "Go to Upload and load your test data first.")
        return

    df = st.session_state.df
    flaky = st.session_state.flaky_results
    
    stats = compute_stats(df)
    section_header("📊", "Flaky Test Table", f"Found {len(flaky)} flaky tests out of {stats['total']}")

    metric_row([
        {"label": "Total Tests",   "value": str(stats["total"]),      "color": PRIMARY},
        {"label": "High Flaky",    "value": str(stats["high_flaky"]),  "color": DANGER},
        {"label": "Medium Flaky",  "value": str(stats["med_flaky"]),   "color": WARN},
        {"label": "Stable",        "value": str(stats["low_flaky"]),   "color": PRIMARY},
        {"label": "Avg Score",     "value": f"{stats['avg_score']:.2f}", "color": ACCENT},
    ])
    
    st.markdown("<br>", unsafe_allow_html=True)

    if not flaky:
        empty_state("👍", "Perfect!", "No flaky tests were detected in this dataset.")
    else:
        # Convert flaky_results back to DataFrame for display
        flaky_df = pd.DataFrame(flaky)
        st.dataframe(flaky_df, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — AI EXPLANATIONS
# ════════════════════════════════════════════════════════════════════════════

def page_ai():
    render_topbar("03 · AI Explanations")
    section_header("🤖", "AI Root Cause Explanations", "Generated by Agent workflow (Ollama)")

    if not os.path.exists(REPORT_PATH):
        empty_state("🤖", "No Report Found", "Go to Agent Execution and run a Full Investigation to generate explanations.")
        return

    try:
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            report_data = json.load(f)
        
        tests = report_data.get("tests", [])
        if not tests:
            empty_state("🤖", "Empty Report", "The generated report contains no flaky tests.")
            return

        for test in tests:
            test_name = test.get("test_name", "Unknown")
            score = float(test.get("flakiness_score", 0))
            severity = test.get("severity", "UNKNOWN")
            root_cause = test.get("root_cause", "No explanation generated.")
            recommended_fix = test.get("recommended_fix", "No fix generated.")
            confidence = test.get("confidence", "N/A")
            
            ai_explanation_card(test_name, root_cause, recommended_fix, confidence, score, severity)
            
    except Exception as e:
        callout(f"Could not load report: {e}", "error")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — AGENT EXECUTION
# ════════════════════════════════════════════════════════════════════════════

def page_agent():
    render_topbar("04 · Agent Execution")
    section_header("⚙️", "Autonomous Workflow Orchestrator", "Execute the full agent pipeline")

    st.markdown("Trigger the `agent.py` script to run the 7-step autonomous investigation workflow.")

    if st.button("🚀 Run Full Investigation", use_container_width=True):
        st.markdown("---")
        log_container = st.empty()
        log_text = ""
        
        # Execute agent.py as a subprocess and stream output
        process = subprocess.Popen(
            [sys.executable, os.path.join(os.path.dirname(__file__), "agent.py")],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        for line in iter(process.stdout.readline, ''):
            log_text += line
            log_container.code(log_text, language="log")

        process.stdout.close()
        process.wait()

        if process.returncode == 0:
            callout("Agent execution completed successfully! Head to AI Explanations to see results.", "success")
        else:
            callout(f"Agent execution failed with return code {process.returncode}.", "error")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 — INVESTIGATION HISTORY
# ════════════════════════════════════════════════════════════════════════════

def page_history():
    render_topbar("05 · Investigation History")
    section_header("📜", "Historical Database", "Loaded directly from SQLite")

    try:
        initialize_database()
        results = get_all_results()
        
        if not results:
            empty_state("📜", "Database is Empty", "No records found in SQLite. Run the agent first.")
            return

        # Convert ORM objects to dicts for DataFrame
        data = []
        for r in results:
            data.append({
                "ID": r.id,
                "Test Name": r.test_name,
                "Flakiness Score": r.flakiness_score,
                "Severity": r.severity,
                "Timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
            
        df = pd.DataFrame(data)
        
        # Sidebar filters
        severity_filter = st.selectbox("Filter Severity", ["All", "HIGH", "MEDIUM", "LOW"])
        if severity_filter != "All":
            df = df[df["Severity"] == severity_filter]
            
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        callout(f"Failed to read from SQLite database: {e}", "error")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 6 — DOWNLOAD REPORTS
# ════════════════════════════════════════════════════════════════════════════

def page_download():
    render_topbar("06 · Download Reports")
    section_header("📥", "Export Report", "Download your AI-powered analysis")

    if not os.path.exists(REPORT_PATH):
        empty_state("📥", "No Report Available", "Run the agent to generate a report.")
        return

    try:
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            report_str = f.read()
            report_data = json.loads(report_str)
            
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown(f"""
            <div class="animate-in" style="background:{BG_CARD};border:1px solid #1E2D45;
                        border-top:3px solid {ACCENT};border-radius:12px;padding:1.4rem;
                        text-align:center;min-height:160px;">
              <div style="font-size:2rem;margin-bottom:0.5rem;">📋</div>
              <div style="font-family:'Space Mono',monospace;font-size:0.82rem;font-weight:700;
                          color:{TEXT_MAIN};margin-bottom:0.4rem;">JSON Export</div>
              <div style="font-size:0.74rem;color:{TEXT_MUTED};margin-bottom:1rem;line-height:1.5;">Structured JSON generated by Agent workflow</div>
            </div>""", unsafe_allow_html=True)
            st.download_button("⬇ Download JSON", data=report_str.encode('utf-8'), file_name=f"flaky_report_{ts}.json",
                               mime="application/json", use_container_width=True)

        with col2:
            # Build markdown report
            tests = report_data.get("tests", [])
            md = [f"# Flaky Test Report\n_Generated: {report_data.get('generated_at', 'Unknown')}_\n"]
            for test in tests:
                md.append(f"## {test.get('test_name')}")
                md.append(f"- **Score**: {test.get('flakiness_score')}")
                md.append(f"- **Severity**: {test.get('severity')}")
                md.append(f"### Root Cause (Confidence: {test.get('confidence')})")
                md.append(test.get('root_cause'))
                md.append(f"### Recommended Fix")
                md.append(test.get('recommended_fix'))
                md.append("\n---\n")

            st.markdown(f"""
            <div class="animate-in" style="background:{BG_CARD};border:1px solid #1E2D45;
                        border-top:3px solid {WARN};border-radius:12px;padding:1.4rem;
                        text-align:center;min-height:160px;">
              <div style="font-size:2rem;margin-bottom:0.5rem;">📝</div>
              <div style="font-family:'Space Mono',monospace;font-size:0.82rem;font-weight:700;
                          color:{TEXT_MAIN};margin-bottom:0.4rem;">Markdown Report</div>
              <div style="font-size:0.74rem;color:{TEXT_MUTED};margin-bottom:1rem;line-height:1.5;">Human-readable report with AI explanations</div>
            </div>""", unsafe_allow_html=True)
            st.download_button("⬇ Download .md", data="\n".join(md).encode('utf-8'), file_name=f"flaky_report_{ts}.md",
                               mime="text/markdown", use_container_width=True)

    except Exception as e:
        callout(f"Error loading report: {e}", "error")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 7 — CHAT
# ════════════════════════════════════════════════════════════════════════════

def page_chat():
    render_topbar("07 · Chat with Data")
    section_header("💬", "Chat with Data", "Ask anything — powered by Local Ollama")

    df = st.session_state.df

    # ── History ──
    if not st.session_state.chat_history:
        empty_state("💬", "Start the conversation", "Type your question below to ask the local AI.")
    else:
        for msg in st.session_state.chat_history:
            chat_bubble(msg["role"], msg["content"])

    # ── Input ──
    st.markdown("<br>", unsafe_allow_html=True)
    inp_col, btn_col = st.columns([5,1])
    with inp_col:
        user_input = st.text_input("", placeholder="Ask about your flaky tests…",
                                   label_visibility="collapsed", key="chat_input")
    with btn_col:
        send = st.button("Send ➤", use_container_width=True)

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Ollama is thinking…"):
            ans = answer_question_with_ai(user_input, df, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": ans})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑 Clear chat"):
            st.session_state.chat_history = []
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# ROUTER
# ════════════════════════════════════════════════════════════════════════════

{
    "upload":   page_upload,
    "table":    page_table,
    "ai":       page_ai,
    "agent":    page_agent,
    "history":  page_history,
    "download": page_download,
    "chat":     page_chat,
}.get(page, page_upload)()
