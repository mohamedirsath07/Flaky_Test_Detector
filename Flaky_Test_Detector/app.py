import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="Flaky Test Detector & Explainer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5, #06b6d4);
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/test-passed.png", width=80)
    st.title("Navigation")
    page = st.radio("Go to", ["Dashboard", "Detection Rules", "LLM Explainer", "Agent Run Logs"])
    st.divider()
    st.markdown("### System Status")
    st.success("Ollama LLM: Connected")
    st.success("SQLite Database: Active")

# Main Header
st.title("🔍 Flaky Test Detector & Explainer")
st.markdown("---")

if page == "Dashboard":
    st.subheader("⚡ Overview Dashboard")
    
    # Placeholder Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>Total Tests</h3><h2>120</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Passed Runs</h3><h2>1,042</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>Failed Runs</h3><h2>58</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3 style="color:#f87171;">Flaky Detected</h3><h2>3</h2></div>', unsafe_allow_html=True)

    st.markdown("### 📊 Flaky Test Scan (Phase 1 Placeholder)")
    st.info("Upload or scan historical execution records to begin detection.")
    
    if st.button("Trigger Scan Pipeline"):
        st.warning("Detection mechanism placeholder triggered! In Phase 2, this will run detector.py & database.py.")

elif page == "Detection Rules":
    st.subheader("🛠️ Flakiness Criteria Configuration")
    st.write("Configure thresholds and settings for detecting flaky tests.")
    st.slider("Minimum Flakiness Score threshold", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
    st.checkbox("Ignore duration flakiness (timing out differences)")

elif page == "LLM Explainer":
    st.subheader("💡 AI Root Cause Analyzer")
    st.write("Generate detailed insights into automated test failures.")
    test_select = st.selectbox("Select Flaky Test to Explain", ["login_test", "search_test", "payment_test"])
    
    if st.button("Run Explainer"):
        st.info(f"Invoking Local LLM for {test_select}...")
        st.warning("Explainer logic is currently a placeholder. In Phase 2, this will invoke explainer.py.")

elif page == "Agent Run Logs":
    st.subheader("🤖 Autonomous Agent Status")
    st.write("Monitor the background orchestration agent logs.")
    st.code("[INFO] 2026-06-08 11:55:00 - Agent initialized.\n[INFO] 2026-06-08 11:55:01 - Awaiting triggers...")
