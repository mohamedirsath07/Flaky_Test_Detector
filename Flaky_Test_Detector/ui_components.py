"""
ui_components.py
Reusable UI building blocks for the Flaky Test Detector & Explainer dashboard.
"""

import streamlit as st

# Color Palette
PRIMARY   = "#0FF4C6"
ACCENT    = "#FF3CAC"
WARN      = "#FFD166"
DANGER    = "#FF4D6D"
BG_DEEP   = "#0A0E1A"
BG_CARD   = "#111827"
BG_LIGHT  = "#1C2333"
TEXT_MAIN = "#E8EDF5"
TEXT_MUTED= "#6B7A99"

def inject_global_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        background: {BG_DEEP} !important;
        color: {TEXT_MAIN};
        font-family: 'DM Sans', sans-serif;
    }}
    [data-testid="stSidebar"] {{
        background: {BG_CARD} !important;
        border-right: 1px solid #1E2D45;
    }}
    [data-testid="stSidebar"] * {{ color: {TEXT_MAIN} !important; }}
    [data-testid="stHeader"] {{ display: none; }}

    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY} 0%, #00C8A0 100%);
        color: {BG_DEEP};
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        font-size: 0.82rem;
        letter-spacing: 0.08em;
        border: none;
        border-radius: 6px;
        padding: 0.55rem 1.4rem;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 24px {PRIMARY}55;
    }}

    .stTextInput input, .stTextArea textarea {{
        background: {BG_LIGHT} !important;
        color: {TEXT_MAIN} !important;
        border: 1px solid #2A3550 !important;
        border-radius: 6px !important;
        font-family: 'DM Sans', sans-serif !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 2px {PRIMARY}33 !important;
    }}

    [data-testid="metric-container"] {{
        background: {BG_CARD};
        border: 1px solid #1E2D45;
        border-radius: 10px;
        padding: 1rem 1.2rem;
    }}

    .stDataFrame {{ border-radius: 10px; overflow: hidden; }}
    thead tr th {{ background: {BG_LIGHT} !important; color: {PRIMARY} !important;
                   font-family: 'Space Mono', monospace !important; font-size: 0.78rem !important; }}
    tbody tr:hover {{ background: #1A2438 !important; }}

    .streamlit-expanderHeader {{
        background: {BG_CARD} !important;
        border: 1px solid #1E2D45 !important;
        border-radius: 8px !important;
        color: {TEXT_MAIN} !important;
        font-family: 'Space Mono', monospace !important;
    }}

    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: {BG_DEEP}; }}
    ::-webkit-scrollbar-thumb {{ background: #2A3550; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {PRIMARY}88; }}
    
    @keyframes fadeSlideIn {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .animate-in {{ animation: fadeSlideIn 0.45s ease both; }}

    .nav-label {{
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.12em;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        padding: 0.5rem 0 0.3rem 0.2rem;
    }}
    </style>
    """, unsafe_allow_html=True)


def render_topbar(page_title: str = ""):
    st.markdown(f"""
    <div class="animate-in" style="
        display:flex; align-items:center; justify-content:space-between;
        padding:0.9rem 1.6rem; margin-bottom:1.4rem;
        background:linear-gradient(90deg,{BG_CARD},{BG_DEEP});
        border-bottom:1px solid #1E2D45; border-radius:0 0 12px 12px;">
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:36px;height:36px;border-radius:8px;
                    background:linear-gradient(135deg,{PRIMARY},{ACCENT});
                    display:flex;align-items:center;justify-content:center;
                    font-size:1.1rem;">⚡</div>
        <div>
          <div style="font-family:'Space Mono',monospace;font-weight:700;
                      font-size:1rem;letter-spacing:0.05em;">
            FLAKY<span style="color:{PRIMARY}">TEST</span>
            <span style="color:{TEXT_MUTED}">DETECTOR</span>
          </div>
          <div style="font-size:0.7rem;color:{TEXT_MUTED};margin-top:-2px;">
            Powered by Ollama (Local)
          </div>
        </div>
      </div>
      <div style="font-family:'Space Mono',monospace;font-size:0.75rem;
                  color:{PRIMARY};background:{PRIMARY}18;
                  border:1px solid {PRIMARY}44;border-radius:20px;
                  padding:0.25rem 0.8rem;">
        {page_title}
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:1rem 0.5rem 0.5rem;">
          <div style="font-family:'Space Mono',monospace;font-size:1.05rem;
                      font-weight:700;color:{TEXT_MAIN};">⚡ FlakyDetect</div>
          <div style="font-size:0.72rem;color:{TEXT_MUTED};margin-top:3px;">
            Local AI Powered
          </div>
        </div>
        <hr style="border-color:#1E2D45;margin:0.8rem 0;">
        <div class="nav-label">Navigation</div>
        """, unsafe_allow_html=True)

        pages = {
            "📂 Upload Data": "upload",
            "📊 Detection Results": "table",
            "🤖 AI Explanations": "ai",
            "⚙ Agent Execution": "agent",
            "📜 Investigation History": "history",
            "📥 Download Reports": "download",
            "💬 Chat With Data": "chat",
        }
        selection = st.radio("", list(pages.keys()), label_visibility="collapsed")
        
        st.markdown("<hr style='border-color:#1E2D45;margin:1rem 0;'>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:{BG_LIGHT};border:1px solid #1E2D45;border-radius:8px;
                    padding:0.8rem;margin-top:0.5rem;">
          <div style="font-family:'Space Mono',monospace;font-size:0.7rem;
                      color:{TEXT_MUTED};letter-spacing:0.1em;">AI ENGINE</div>
          <div style="display:flex;align-items:center;gap:6px;margin-top:6px;">
            <div style="width:7px;height:7px;border-radius:50%;
                        background:{PRIMARY};"></div>
            <span style="font-size:0.78rem;color:{TEXT_MAIN};">Ollama Local</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        return pages[selection]


def section_header(icon: str, title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="animate-in" style="margin-bottom:1.2rem;">
      <div style="display:flex;align-items:center;gap:10px;">
        <span style="font-size:1.4rem;">{icon}</span>
        <div>
          <h2 style="margin:0;font-family:'Space Mono',monospace;font-size:1.1rem;
                     font-weight:700;color:{TEXT_MAIN};">{title}</h2>
          {"<p style='margin:2px 0 0;font-size:0.8rem;color:"+TEXT_MUTED+";'>"+subtitle+"</p>" if subtitle else ""}
        </div>
      </div>
      <div style="height:2px;background:linear-gradient(90deg,{PRIMARY}88,transparent);
                  border-radius:2px;margin-top:10px;"></div>
    </div>
    """, unsafe_allow_html=True)


def metric_row(metrics: list):
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        color = m.get("color", PRIMARY)
        col.markdown(f"""
        <div class="animate-in" style="background:{BG_CARD};border:1px solid #1E2D45;
                    border-left:3px solid {color};border-radius:10px;padding:1rem 1.2rem;">
          <div style="font-size:0.72rem;color:{TEXT_MUTED};font-family:'Space Mono',monospace;
                      letter-spacing:0.08em;text-transform:uppercase;">{m['label']}</div>
          <div style="font-size:1.7rem;font-weight:700;color:{color};
                      font-family:'Space Mono',monospace;line-height:1.2;margin-top:4px;">{m['value']}</div>
        </div>
        """, unsafe_allow_html=True)


def score_badge(score: float) -> str:
    # Convert flakiness score (0.0 - 1.0) to percentage (0 - 100)
    score_pct = int(score * 100)
    if score >= 0.75:
        color, label = DANGER, "HIGH"
    elif score >= 0.40:
        color, label = WARN, "MED"
    else:
        color, label = PRIMARY, "LOW"
    return f"""
    <div style="display:flex;align-items:center;gap:8px;">
      <div style="width:80px;height:6px;background:#1E2D45;border-radius:3px;overflow:hidden;">
        <div style="width:{score_pct}%;height:100%;background:{color};border-radius:3px;"></div>
      </div>
      <span style="font-family:'Space Mono',monospace;font-size:0.78rem;color:{color};
                   min-width:32px;">{score_pct}</span>
      <span style="font-size:0.65rem;background:{color}22;color:{color};border:1px solid {color}55;
                   border-radius:4px;padding:1px 5px;font-family:'Space Mono',monospace;">{label}</span>
    </div>"""


def upload_card(label: str, file_type: str, icon: str, accept: list):
    st.markdown(f"""
    <div class="animate-in" style="background:{BG_CARD};border:1px solid #1E2D45;
                border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:0.6rem;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.6rem;">
        <span style="font-size:1.2rem;">{icon}</span>
        <span style="font-family:'Space Mono',monospace;font-size:0.82rem;color:{TEXT_MAIN};">{label}</span>
        <span style="font-size:0.68rem;background:{PRIMARY}18;color:{PRIMARY};
                     border:1px solid {PRIMARY}44;border-radius:4px;padding:1px 6px;
                     font-family:'Space Mono',monospace;">{file_type}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    return st.file_uploader("", type=accept, key=f"upload_{file_type}", label_visibility="collapsed")


def callout(text: str, kind: str = "info"):
    colors = {"info": (PRIMARY, "ℹ"), "warn": (WARN, "⚠"), "error": (DANGER, "✕"), "success": (PRIMARY, "✓")}
    c, icon = colors.get(kind, colors["info"])
    st.markdown(f"""
    <div class="animate-in" style="background:{c}0F;border:1px solid {c}44;border-radius:8px;
                padding:0.75rem 1rem;display:flex;gap:10px;align-items:flex-start;margin:0.5rem 0;">
      <span style="color:{c};font-size:0.9rem;margin-top:1px;">{icon}</span>
      <span style="font-size:0.82rem;color:{TEXT_MAIN};line-height:1.5;">{text}</span>
    </div>
    """, unsafe_allow_html=True)


def ai_explanation_card(test_name: str, root_cause: str, recommended_fix: str, confidence: str, score: float, severity: str):
    tier_colors = {"HIGH": DANGER, "MEDIUM": WARN, "LOW": PRIMARY, "UNKNOWN": TEXT_MUTED}
    tc = tier_colors.get(severity.upper(), PRIMARY)
    
    # Check if confidence is a percentage string or already a string
    conf_str = confidence if isinstance(confidence, str) else f"{confidence}%"
    
    st.markdown(f"""
    <div class="animate-in" style="display:flex;gap:12px;margin:1rem 0;flex-wrap:wrap;">
      <div style="background:{tc}18;border:1px solid {tc}44;border-radius:8px;
                  padding:0.6rem 1rem;display:flex;align-items:center;gap:8px;">
        <span style="font-size:0.72rem;color:{tc};font-family:'Space Mono',monospace;">SEVERITY</span>
        <span style="font-family:'Space Mono',monospace;font-weight:700;color:{tc};">{severity.upper()}</span>
      </div>
      <div style="background:{PRIMARY}18;border:1px solid {PRIMARY}44;border-radius:8px;
                  padding:0.6rem 1rem;display:flex;align-items:center;gap:8px;">
        <span style="font-size:0.72rem;color:{PRIMARY};font-family:'Space Mono',monospace;">CONFIDENCE</span>
        <span style="font-family:'Space Mono',monospace;font-weight:700;color:{PRIMARY};">{conf_str}</span>
      </div>
      <div style="background:{BG_CARD};border:1px solid #1E2D45;border-radius:8px;
                  padding:0.6rem 1rem;display:flex;align-items:center;gap:8px;">
        <span style="font-size:0.72rem;color:{TEXT_MUTED};font-family:'Space Mono',monospace;">SCORE</span>
        <span style="font-family:'Space Mono',monospace;font-weight:700;color:{tc};">{score:.2f}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="animate-in" style="background:{BG_CARD};border:1px solid #1E2D45;border-radius:12px;overflow:hidden;margin-bottom:1.5rem;">
      <div style="background:#1A2438;padding:0.8rem 1.2rem;border-bottom:1px solid #1E2D45;
                  display:flex;align-items:center;gap:10px;">
        <span style="color:{PRIMARY};">🔬</span>
        <span style="font-family:'Space Mono',monospace;font-size:0.9rem;font-weight:700;color:{TEXT_MAIN};">{test_name}</span>
      </div>
      <div style="padding:1.2rem;">
        <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:{TEXT_MUTED};margin-bottom:0.4rem;">ROOT CAUSE</div>
        <div style="font-size:0.9rem;color:{TEXT_MAIN};line-height:1.6;margin-bottom:1.2rem;white-space:pre-wrap;">{root_cause}</div>
        
        <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:{TEXT_MUTED};margin-bottom:0.4rem;">RECOMMENDED FIX</div>
        <div style="font-size:0.9rem;color:{TEXT_MAIN};line-height:1.6;white-space:pre-wrap;
                    background:{BG_LIGHT};padding:1rem;border-radius:8px;border-left:3px solid {PRIMARY};">{recommended_fix}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def empty_state(icon: str, title: str, description: str):
    st.markdown(f"""
    <div class="animate-in" style="text-align:center;padding:4rem 2rem;">
      <div style="font-size:3rem;margin-bottom:1rem;opacity:0.8;">{icon}</div>
      <h3 style="margin:0 0 0.5rem;font-family:'Space Mono',monospace;color:{TEXT_MAIN};">{title}</h3>
      <p style="color:{TEXT_MUTED};font-size:0.9rem;max-width:400px;margin:0 auto;">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def chat_bubble(role: str, content: str):
    is_user = role == "user"
    align = "flex-end" if is_user else "flex-start"
    bg = f"{PRIMARY}1A" if is_user else BG_CARD
    border = f"1px solid {PRIMARY}44" if is_user else "1px solid #1E2D45"
    br = "16px 16px 0 16px" if is_user else "16px 16px 16px 0"
    
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:{align};margin-bottom:1rem;">
      <div style="font-size:0.7rem;color:{TEXT_MUTED};margin-bottom:4px;margin-left:8px;margin-right:8px;">
        {'You' if is_user else 'AI Assistant'}
      </div>
      <div class="animate-in" style="background:{bg}; border:{border}; border-radius:{br}; 
                  padding:0.8rem 1.2rem; max-width:85%; font-size:0.9rem; color:{TEXT_MAIN}; 
                  line-height:1.5; white-space:pre-wrap;">
        {content}
      </div>
    </div>
    """, unsafe_allow_html=True)
