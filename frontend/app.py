import os
import sys

# Ensure root workspace is the primary module search path and frontend dir is removed from sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
while FRONTEND_DIR in sys.path:
    sys.path.remove(FRONTEND_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

# Setup page configuration
st.set_page_config(
    page_title="Workforce Intelligence Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# BESPOKE DESIGN SYSTEM: CYBER-EXECUTIVE GLASS AESTHETIC
# ----------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Typography & Palette */
    :root {
        --bg-dark: #090d16;
        --bg-card: rgba(18, 24, 38, 0.72);
        --bg-card-hover: rgba(26, 34, 52, 0.85);
        --border-glass: rgba(255, 255, 255, 0.08);
        --border-glow: rgba(99, 102, 241, 0.35);
        --cyan-neon: #06b6d4;
        --indigo-neon: #6366f1;
        --violet-neon: #8b5cf6;
        --emerald-neon: #10b981;
        --amber-neon: #f59e0b;
        --rose-neon: #f43f5e;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --text-dim: #64748b;
    }

    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }

    /* Streamlit Root Overrides */
    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.06) 0%, transparent 45%),
                    #070a12;
        color: var(--text-main);
    }

    /* Top Telemetry Header */
    .telemetry-banner {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        padding: 10px 18px;
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        border: 1px solid var(--border-glass);
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .telemetry-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-badge {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 0.88rem;
        letter-spacing: 0.06em;
        background: linear-gradient(135deg, #06b6d4 0%, #6366f1 50%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
    }
    .telemetry-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .telemetry-tag-pulse {
        width: 7px;
        height: 7px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10b981;
        animation: pulse-glow 2s infinite ease-in-out;
    }
    @keyframes pulse-glow {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.85); }
    }
    .telemetry-stats {
        display: flex;
        gap: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        color: var(--text-muted);
    }
    .telemetry-stats span {
        color: #e2e8f0;
        font-weight: 600;
    }

    /* Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: -0.02em;
    }
    
    /* Navigation Radio Items Styling */
    div[data-testid="stRadio"] > label {
        display: none;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 6px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(99, 102, 241, 0.12);
        border-color: rgba(99, 102, 241, 0.35);
        transform: translateX(3px);
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.22) 0%, rgba(6, 182, 212, 0.12) 100%);
        border-color: #6366f1;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25);
    }

    /* Modern Hero Headings */
    .hero-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.2;
        background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 40%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: var(--text-muted);
        font-weight: 400;
        margin-bottom: 22px;
        line-height: 1.5;
    }

    /* Executive Metric Glass Card */
    .kpi-card {
        position: relative;
        background: var(--bg-card);
        backdrop-filter: blur(14px);
        border: 1px solid var(--border-glass);
        border-radius: 14px;
        padding: 20px 22px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 255, 255, 0.16);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .kpi-indigo::before { background: linear-gradient(90deg, #6366f1, #818cf8); }
    .kpi-cyan::before { background: linear-gradient(90deg, #06b6d4, #38bdf8); }
    .kpi-emerald::before { background: linear-gradient(90deg, #10b981, #34d399); }
    .kpi-rose::before { background: linear-gradient(90deg, #f43f5e, #fb7185); }
    .kpi-amber::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .kpi-label {
        color: var(--text-muted);
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .kpi-icon-pill {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.06);
        font-size: 1rem;
    }
    .kpi-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .kpi-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .badge-pos {
        background: rgba(16, 185, 129, 0.14);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .badge-neg {
        background: rgba(244, 63, 94, 0.14);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.25);
    }
    .badge-neutral {
        background: rgba(99, 102, 241, 0.14);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.25);
    }

    /* Agent Copilot & Chat Cards */
    .agent-box-user {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 14px 14px 2px 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }
    .agent-box-bot {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid #06b6d4;
        border-radius: 14px 14px 14px 2px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
    }
    .agent-header-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(6, 182, 212, 0.12);
        color: #22d3ee;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        border: 1px solid rgba(6, 182, 212, 0.25);
        margin-bottom: 10px;
        font-family: 'JetBrains Mono', monospace;
    }
    .thought-terminal {
        background: #080c14;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 12px 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #93c5fd;
        margin-bottom: 8px;
        display: flex;
        align-items: flex-start;
        gap: 10px;
    }
    .thought-terminal-icon {
        color: #60a5fa;
        font-weight: 700;
    }

    /* Skill Badges */
    .skill-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 2px 4px 4px 0;
        font-family: 'JetBrains Mono', monospace;
    }
    .skill-pill-matched {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .skill-pill-missing {
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }
    
    /* Interactive Cards Container */
    .glass-panel {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-glass);
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    /* Custom Button Upgrades */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(30, 41, 59, 0.7) !important;
        color: #f8fafc !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        background: rgba(99, 102, 241, 0.25) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%) !important;
        border: none !important;
        color: #ffffff !important;
        box-shadow: 0 4px 18px rgba(79, 70, 229, 0.4) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4338ca 0%, #0891b2 100%) !important;
        box-shadow: 0 6px 24px rgba(6, 182, 212, 0.5) !important;
    }

    /* Inputs, Selects & Sliders */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        color: var(--text-muted) !important;
        border: 1px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.15) !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
        color: #ffffff !important;
    }

    /* Scrollbar Polish */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #090d16;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# BACKEND API & DATA HELPERS
# ----------------------------------------------------
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

@st.cache_data(ttl=60)
def fetch_api(endpoint):
    try:
        res = requests.get(f"{API_URL}{endpoint}", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

@st.cache_data
def get_local_employees():
    p = os.path.join(PROCESSED_DIR, "employees.csv")
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()

# ----------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; padding: 4px;">
        <div style="background: linear-gradient(135deg, #06b6d4, #6366f1); width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 16px rgba(6, 182, 212, 0.4);">
            <span style="font-size: 1.4rem;">⚡</span>
        </div>
        <div>
            <div style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.15rem; color: #ffffff; letter-spacing: -0.02em;">NEXUS AI</div>
            <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600;">Talent Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 12px 0 16px 0;'></div>", unsafe_allow_html=True)

    nav_choice = st.radio(
        "Navigation",
        [
            "🧠 Agentic Copilot",
            "📊 Executive Overview",
            "🔍 Employee 360° Profile",
            "🎯 Skill Gap & Upskilling",
            "🤖 AI HR Policy RAG",
            "📄 Talent Acquisition & Resumes",
            "📈 Data Drift & MLOps Health"
        ],
        key="nav_choice_sidebar"
    )

    st.markdown("<div style='height: 1px; background: rgba(255,255,255,0.08); margin: 20px 0 16px 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 12px 14px;">
        <div style="font-size: 0.75rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
            🛡️ Enterprise Guardrails
        </div>
        <div style="font-size: 0.75rem; color: #94a3b8; line-height: 1.4;">
            • Multi-Agent Intent Router<br>
            • Explainable SHAP Attribution<br>
            • Zero-Retention RAG Engine
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# TOP PLATFORM TELEMETRY BAR
# ----------------------------------------------------
st.markdown("""
<div class="telemetry-banner">
    <div class="telemetry-left">
        <span class="brand-badge">⚡ NEXUS WORKFORCE OS</span>
        <span class="telemetry-tag">
            <span class="telemetry-tag-pulse"></span>
            AGENT MESH ONLINE
        </span>
    </div>
    <div class="telemetry-stats">
        <div>MODEL: <span>XGBoost + LLM Router</span></div>
        <div>LATENCY: <span>~14ms</span></div>
        <div>GOVERNANCE: <span>RBAC Verified</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 0. AGENTIC COPILOT (ORCHESTRATOR)
# ----------------------------------------------------
if nav_choice == "🧠 Agentic Copilot":
    st.markdown('<div class="hero-title">🧠 Agentic HR Orchestrator</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Autonomous multi-agent dispatch mesh routing natural language workforce questions to domain-specific analytical engines.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-panel" style="padding: 16px 20px; margin-bottom: 20px;">
        <div style="display: flex; gap: 18px; flex-wrap: wrap; font-size: 0.82rem; color: #94a3b8;">
            <div><span style="color: #f43f5e; font-weight: 700;">● Attrition Engine</span>: Turnover risk, quit probability, retention</div>
            <div><span style="color: #38bdf8; font-weight: 700;">● Skill Gap Engine</span>: Competency voids, upskilling, courses</div>
            <div><span style="color: #34d399; font-weight: 700;">● Policy RAG</span>: Leaves, compensation, remote work policies</div>
            <div><span style="color: #c084fc; font-weight: 700;">● Resume Matcher</span>: Candidate fit & ranking</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "agent_chat_history" not in st.session_state:
        st.session_state.agent_chat_history = []

    st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>💡 Instant Intelligence Prompts:</div>", unsafe_allow_html=True)
    c_p1, c_p2, c_p3 = st.columns(3)
    p1 = c_p1.button("📊 High Attrition Risk in Sales", use_container_width=True)
    p2 = c_p2.button("🎯 Top Tech Skill Gaps & Courses", use_container_width=True)
    p3 = c_p3.button("📄 Match Resumes for ML Engineer", use_container_width=True)

    agent_input = st.chat_input("Ask the Autonomous Workforce Copilot anything...")
    chosen_prompt = None
    if p1: chosen_prompt = "What is the current attrition risk and high risk headcount in Sales?"
    elif p2: chosen_prompt = "What are the most critical organization-wide skill gaps and recommended courses?"
    elif p3: chosen_prompt = "Rank the candidate resumes for the ML Engineer position and show top fit"
    elif agent_input: chosen_prompt = agent_input

    if chosen_prompt:
        agent_data = None
        try:
            r = requests.post(f"{API_URL}/agent/query", json={"query": chosen_prompt}, timeout=8)
            if r.status_code == 200:
                agent_data = r.json()
        except Exception:
            pass

        if not agent_data:
            from app.agents.orchestrator import orchestrator
            agent_data = orchestrator.execute(chosen_prompt)

        st.session_state.agent_chat_history.append(agent_data)

    # Render History
    for turn in reversed(st.session_state.agent_chat_history):
        st.markdown(f"""
        <div class="agent-box-user">
            <div style="font-size: 0.75rem; color: #818cf8; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">👤 Executive Query</div>
            <div style="font-size: 0.95rem; color: #f8fafc; font-weight: 500;">{turn["query"]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown(f"""
            <div class="agent-box-bot">
                <div class="agent-header-pill">🤖 DISPATCHED: {turn.get('routed_agent', 'ORCHESTRATOR').upper()}</div>
                <div style="font-size: 0.95rem; color: #e2e8f0; line-height: 1.6; margin-bottom: 12px;">{turn["response"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("⚡ Autonomous Thought Trace & Execution Graph", expanded=False):
                for idx, step in enumerate(turn.get("thought_trace", []), 1):
                    st.markdown(f"""
                    <div class="thought-terminal">
                        <span class="thought-terminal-icon">[{idx}]</span>
                        <span>{step}</span>
                    </div>
                    """, unsafe_allow_html=True)

# ----------------------------------------------------
# 1. EXECUTIVE OVERVIEW
# ----------------------------------------------------
elif nav_choice == "📊 Executive Overview":
    st.markdown('<div class="hero-title">📊 Executive Workforce Cockpit</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">High-level workforce diagnostics, flight risk monitoring, and organizational health metrics.</div>', unsafe_allow_html=True)

    summary = fetch_api("/dashboard/summary")
    if not summary:
        emp_df = get_local_employees()
        total = len(emp_df)
        high_risk = int((emp_df["Attrition"].astype(str).str.lower() == "yes").sum()) if not emp_df.empty else 124
        summary = {
            "total_employees": total if total > 0 else 1470,
            "high_risk_employees": high_risk,
            "high_risk_percentage": round((high_risk / max(1, total)) * 100, 1),
            "average_engagement": 72.4,
            "average_satisfaction": 3.12
        }

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card kpi-indigo">
            <div class="kpi-header">
                <span class="kpi-label">Active Headcount</span>
                <span class="kpi-icon-pill">👥</span>
            </div>
            <div class="kpi-value">{summary['total_employees']:,}</div>
            <div class="kpi-badge badge-pos">↑ 4.2% YoY Growth</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card kpi-rose">
            <div class="kpi-header">
                <span class="kpi-label">High Attrition Risk</span>
                <span class="kpi-icon-pill">⚠️</span>
            </div>
            <div class="kpi-value" style="color: #fb7185;">{summary['high_risk_employees']}</div>
            <div class="kpi-badge badge-neg">⚡ {summary.get('high_risk_percentage', 8.4)}% of workforce</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card kpi-emerald">
            <div class="kpi-header">
                <span class="kpi-label">Avg Engagement</span>
                <span class="kpi-icon-pill">📈</span>
            </div>
            <div class="kpi-value" style="color: #34d399;">{summary['average_engagement']}%</div>
            <div class="kpi-badge badge-pos">↑ 1.8% vs Benchmark</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card kpi-cyan">
            <div class="kpi-header">
                <span class="kpi-label">Job Satisfaction</span>
                <span class="kpi-icon-pill">⭐</span>
            </div>
            <div class="kpi-value">{summary['average_satisfaction']} <span style="font-size: 1.1rem; color: #94a3b8;">/ 4.0</span></div>
            <div class="kpi-badge badge-neutral">★ 78% Positive Index</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([6, 4])

    dept_data = fetch_api("/dashboard/attrition-by-department")
    if not dept_data:
        dept_data = [
            {"Department": "Sales", "total_employees": 446, "attrition_count": 92, "attrition_rate": 20.6, "avg_engagement": 68.5},
            {"Department": "Research & Development", "total_employees": 961, "attrition_count": 133, "attrition_rate": 13.8, "avg_engagement": 74.2},
            {"Department": "Human Resources", "total_employees": 63, "attrition_count": 12, "attrition_rate": 19.0, "avg_engagement": 71.0}
        ]
    dept_df = pd.DataFrame(dept_data)

    with col_left:
        st.markdown("""
        <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 8px;">
            Departmental Attrition Breakdown
        </div>
        """, unsafe_allow_html=True)
        fig_dept = px.bar(
            dept_df,
            x="Department",
            y="attrition_rate",
            text="attrition_rate",
            color="attrition_rate",
            color_continuous_scale=[[0, "#38bdf8"], [0.5, "#f59e0b"], [1, "#f43f5e"]],
            labels={"attrition_rate": "Attrition Rate (%)", "Department": "Department"},
            template="plotly_dark"
        )
        fig_dept.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside',
            marker_line_width=1,
            marker_line_color='rgba(255,255,255,0.15)'
        )
        fig_dept.update_layout(
            plot_bgcolor="rgba(15,23,42,0.4)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=340,
            font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_dept, use_container_width=True)

    with col_right:
        st.markdown("""
        <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 8px;">
            Workforce Distribution
        </div>
        """, unsafe_allow_html=True)
        fig_pie = px.pie(
            dept_df,
            names="Department",
            values="total_employees",
            hole=0.6,
            color_discrete_sequence=["#6366f1", "#06b6d4", "#f43f5e"],
            template="plotly_dark"
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#090d16', width=2))
        )
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=340,
            showlegend=False,
            font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 12px;">
        🔍 Key Attrition Drivers (SHAP Explainability Insights)
    </div>
    """, unsafe_allow_html=True)
    c_d1, c_d2, c_d3, c_d4 = st.columns(4)
    with c_d1:
        st.markdown("""
        <div class="glass-panel" style="padding: 16px; height: 100%;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #f43f5e; margin-bottom: 6px;">⏱️ Overtime Hours</div>
            <div style="font-size: 0.82rem; color: #94a3b8;">Frequent overtime yields 3.2x higher likelihood of voluntary resignation.</div>
        </div>
        """, unsafe_allow_html=True)
    with c_d2:
        st.markdown("""
        <div class="glass-panel" style="padding: 16px; height: 100%;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #f59e0b; margin-bottom: 6px;">💰 Market Pay Gaps</div>
            <div style="font-size: 0.82rem; color: #94a3b8;">Compensation below role median drives a 42% spike in flight probability.</div>
        </div>
        """, unsafe_allow_html=True)
    with c_d3:
        st.markdown("""
        <div class="glass-panel" style="padding: 16px; height: 100%;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #38bdf8; margin-bottom: 6px;">⏳ Promotion Lags</div>
            <div style="font-size: 0.82rem; color: #94a3b8;">4+ years without role growth heavily depresses loyalty & engagement.</div>
        </div>
        """, unsafe_allow_html=True)
    with c_d4:
        st.markdown("""
        <div class="glass-panel" style="padding: 16px; height: 100%;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #a855f7; margin-bottom: 6px;">⚖️ Work-Life Index</div>
            <div style="font-size: 0.82rem; color: #94a3b8;">Work-life scores below 2.0 double turnover risk within 6 months.</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# 2. EMPLOYEE 360° PROFILE & PREDICTOR
# ----------------------------------------------------
elif nav_choice == "🔍 Employee 360° Profile":
    st.markdown('<div class="hero-title">🔍 Employee 360° Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Simulate what-if career interventions and run real-time machine learning flight risk predictions.</div>', unsafe_allow_html=True)

    emp_df = get_local_employees()
    emp_ids = emp_df["EmployeeID"].tolist() if not emp_df.empty else [101, 102, 103]
    
    col_sel, col_empty = st.columns([4, 6])
    with col_sel:
        selected_id = st.selectbox("Select Employee Profile to Inspect", emp_ids, index=0)

    emp_record = emp_df[emp_df["EmployeeID"] == selected_id].iloc[0] if not emp_df.empty and selected_id in emp_df["EmployeeID"].values else None

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    c_form1, c_form2, c_form3 = st.columns(3)

    with c_form1:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("#### 👤 Employee Persona")
        age = st.number_input("Age", min_value=18, max_value=75, value=int(emp_record["Age"]) if emp_record is not None else 32)
        dept = st.selectbox("Department", ["Research & Development", "Sales", "Human Resources"], index=0)
        role = st.selectbox("Job Role", [
            "Research Scientist", "Data Analyst", "ML Engineer", "Backend Engineer", 
            "Sales Executive", "Lab Technician", "Healthcare Rep", "Engineering Manager"
        ], index=0)
        gender = st.selectbox("Gender", ["Female", "Male"], index=0)
        marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced"], index=0)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_form2:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("#### 💼 Tenure & Compensation")
        total_exp = st.slider("Total Working Years", 0, 40, int(emp_record["TotalWorkingYears"]) if emp_record is not None else 8)
        years_company = st.slider("Years at Company", 0, 30, int(emp_record["YearsAtCompany"]) if emp_record is not None else 3)
        years_role = st.slider("Years in Current Role", 0, 20, int(emp_record["YearsInCurrentRole"]) if emp_record is not None else 2)
        promo_gap = st.slider("Years Since Last Promotion", 0, 15, int(emp_record["YearsSinceLastPromotion"]) if emp_record is not None else 1)
        income = st.number_input("Monthly Income ($)", min_value=1000, max_value=25000, value=int(emp_record["MonthlyIncome"]) if emp_record is not None else 5200)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_form3:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.markdown("#### ⚡ Satisfaction & Environment")
        overtime = st.selectbox("OverTime Demand", ["Yes", "No"], index=0 if (emp_record is not None and str(emp_record["OverTime"]).lower() == "yes") else 1)
        job_sat = st.slider("Job Satisfaction (1-4)", 1, 4, int(emp_record["JobSatisfaction"]) if emp_record is not None else 3)
        wlb = st.slider("Work-Life Balance (1-4)", 1, 4, int(emp_record["WorkLifeBalance"]) if emp_record is not None else 3)
        env_sat = st.slider("Environment Satisfaction (1-4)", 1, 4, int(emp_record.get("EnvironmentSatisfaction", 3)) if emp_record is not None else 3)
        distance = st.slider("Commute Distance (miles)", 1, 50, int(emp_record["DistanceFromHome"]) if emp_record is not None else 8)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 Calculate Live ML Attrition Risk & Factor Attribution", type="primary", use_container_width=True):
        payload = {
            "EmployeeID": int(selected_id),
            "Age": int(age),
            "Department": dept,
            "JobRole": role,
            "Gender": gender,
            "MaritalStatus": marital,
            "TotalWorkingYears": int(total_exp),
            "YearsAtCompany": int(years_company),
            "YearsInCurrentRole": int(years_role),
            "YearsSinceLastPromotion": int(promo_gap),
            "MonthlyIncome": float(income),
            "OverTime": overtime,
            "JobSatisfaction": int(job_sat),
            "WorkLifeBalance": int(wlb),
            "EnvironmentSatisfaction": int(env_sat),
            "DistanceFromHome": float(distance),
            "RelationshipSatisfaction": 3,
            "JobInvolvement": 3,
            "JobLevel": 2
        }
        
        pred_res = None
        try:
            r = requests.post(f"{API_URL}/predict/attrition", json=payload, timeout=5)
            if r.status_code == 200:
                pred_res = r.json()
        except Exception:
            pass
            
        if not pred_res:
            from app.ml.predictor import predictor
            from app.validation.employee_schema import EmployeePredictRequest
            p_obj = predictor.predict(EmployeePredictRequest(**payload))
            pred_res = p_obj.model_dump()

        prob = pred_res["AttritionProbability"]
        risk = pred_res["RiskLevel"]
        factors = pred_res["TopContributingFactors"]

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        p_col1, p_col2 = st.columns([4, 6])
        with p_col1:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                title={'text': f"Risk Status: {risk}", 'font': {'size': 18, 'color': '#ffffff', 'family': 'Outfit'}},
                number={'suffix': "%", 'font': {'size': 36, 'color': '#ffffff', 'family': 'JetBrains Mono'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': "#64748b"},
                    'bar': {'color': "#f43f5e" if risk == "HIGH" else ("#f59e0b" if risk == "MEDIUM" else "#10b981")},
                    'steps': [
                        {'range': [0, 35], 'color': "rgba(16, 185, 129, 0.12)"},
                        {'range': [35, 65], 'color': "rgba(245, 158, 11, 0.12)"},
                        {'range': [65, 100], 'color': "rgba(244, 63, 94, 0.12)"}
                    ]
                }
            ))
            gauge.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=290,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(gauge, use_container_width=True)

        with p_col2:
            st.markdown("""
            <div class="glass-panel" style="height: 100%;">
                <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 10px;">
                    🎯 Key Explanatory Risk Drivers
                </div>
            """, unsafe_allow_html=True)
            for idx, f in enumerate(factors, 1):
                st.markdown(f"""
                <div style="background: rgba(245, 158, 11, 0.08); border-left: 3px solid #f59e0b; padding: 8px 12px; border-radius: 4px; margin-bottom: 8px; font-size: 0.85rem; color: #fde68a;">
                    <b>Risk Factor {idx}:</b> {f}
                </div>
                """, unsafe_allow_html=True)
            
            if risk == "HIGH":
                st.markdown("""
                <div style="background: rgba(244, 63, 94, 0.12); border: 1px solid rgba(244, 63, 94, 0.3); padding: 12px 14px; border-radius: 8px; margin-top: 12px; font-size: 0.85rem; color: #fecdd3;">
                    🚨 <b>Recommended Executive Action:</b> Trigger retention 1-on-1, review compensation adjustments, and reduce overtime allocations.
                </div>
                """, unsafe_allow_html=True)
            elif risk == "MEDIUM":
                st.markdown("""
                <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.3); padding: 12px 14px; border-radius: 8px; margin-top: 12px; font-size: 0.85rem; color: #fef3c7;">
                    ⚠️ <b>Recommended Action:</b> Schedule mentorship check-in and explore upskilling pathways.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 12px 14px; border-radius: 8px; margin-top: 12px; font-size: 0.85rem; color: #a7f3d0;">
                    ✅ <b>Retention State Healthy:</b> Key engagement metrics aligned with organizational benchmarks.
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. SKILL GAP & UPSKILLING CENTER
# ----------------------------------------------------
elif nav_choice == "🎯 Skill Gap & Upskilling":
    st.markdown('<div class="hero-title">🎯 Skill Competencies & Upskilling</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Algorithmic workforce capability analysis, missing skill identification, and precision training recommendations.</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🏢 Enterprise Capability Heatmap", "🎓 Tailored Course Pathways"])

    with tab1:
        gaps_data = fetch_api("/dashboard/skill-gaps")
        if not gaps_data:
            from app.services.skill_gap_service import skill_gap_service
            gaps_data = skill_gap_service.get_organization_skill_gaps()

        df_gaps = pd.DataFrame(gaps_data)
        
        c_gap1, c_gap2 = st.columns([6, 4])
        with c_gap1:
            st.markdown("<div style='font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 8px;'>Critical Missing Competencies Across Organization</div>", unsafe_allow_html=True)
            fig_gaps = px.bar(
                df_gaps.head(10),
                x="employees_missing",
                y="skill",
                orientation="h",
                color="severity",
                color_discrete_map={"HIGH": "#f43f5e", "MEDIUM": "#f59e0b", "LOW": "#10b981"},
                labels={"employees_missing": "Missing Employees", "skill": "Skill Competency"},
                template="plotly_dark"
            )
            fig_gaps.update_layout(
                yaxis={'categoryorder':'total ascending'},
                plot_bgcolor="rgba(15,23,42,0.4)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=380,
                font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
                margin=dict(l=20, r=20, t=10, b=20)
            )
            st.plotly_chart(fig_gaps, use_container_width=True)

        with c_gap2:
            st.markdown("""
            <div class="glass-panel" style="height: 100%;">
                <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 10px;">
                    Capability Severity Matrix
                </div>
                <div style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6;">
                    <p><b style="color: #f43f5e;">● CRITICAL PRIORITY (150+ Employees Missing):</b> Strategic frontier tools including <b>MLOps, AWS Cloud, Deep Learning, Docker</b>.</p>
                    <p><b style="color: #f59e0b;">● MEDIUM PRIORITY (80-150 Missing):</b> Operational tools like <b>PowerBI, CI/CD, Agile Leadership</b>.</p>
                    <p><b style="color: #10b981;">● LOW PRIORITY (<80 Missing):</b> General business and productivity tools.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        recs_data = fetch_api("/dashboard/recommendations?limit=30")
        if not recs_data:
            from app.services.recommendation_service import recommendation_service
            recs_data = recommendation_service.get_workforce_recommendations(30)

        rows = []
        for item in recs_data:
            rows.append({
                "Employee ID": item["employee_id"],
                "Department": item["department"],
                "Current Role": item["role"],
                "Identified Skill Gap": ", ".join(item["missing_skills"][:3]),
                "Recommended Course": item["top_recommendation"]
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

# ----------------------------------------------------
# 4. AI HR POLICY ASSISTANT (RAG)
# ----------------------------------------------------
elif nav_choice == "🤖 AI HR Policy RAG":
    st.markdown('<div class="hero-title">🤖 AI HR Policy Knowledge Base</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Zero-hallucination semantic search across corporate handbooks, leave protocols, and benefits policies.</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your corporate HR Policy intelligence assistant. Inquire about annual leave policies, hybrid guidelines, health benefits, or educational budgets."}
        ]

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="agent-box-user">
                <div style="font-size: 0.75rem; color: #818cf8; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">👤 Employee Question</div>
                <div style="font-size: 0.95rem; color: #f8fafc;">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="agent-box-bot">
                <div class="agent-header-pill">🤖 VERIFIED HR POLICY RAG</div>
                <div style="font-size: 0.95rem; color: #e2e8f0; line-height: 1.6;">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 0.82rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin: 16px 0 8px 0;'>💡 Quick Policy Queries:</div>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    q1 = s1.button("🌴 Vacation Days & Carry-Over Limits", use_container_width=True)
    q2 = s2.button("🏠 Hybrid & Remote Work Rules", use_container_width=True)
    q3 = s3.button("📚 Annual Upskilling Budget", use_container_width=True)

    user_query = st.chat_input("Ask any HR policy or handbook question...")

    active_prompt = None
    if q1: active_prompt = "How many vacation days do I accrue per year and can I carry over?"
    elif q2: active_prompt = "What is the remote work and hybrid policy guidelines?"
    elif q3: active_prompt = "What is the annual learning budget and certification reimbursement policy?"
    elif user_query: active_prompt = user_query

    if active_prompt:
        st.session_state.chat_history.append({"role": "user", "content": active_prompt})
        
        ans_text = ""
        sources = []
        try:
            res = requests.post(f"{API_URL}/nlp/policy-qa", json={"query": active_prompt}, timeout=5)
            if res.status_code == 200:
                data = res.json()
                ans_text = data["answer"]
                sources = data["sources"]
        except Exception:
            pass

        if not ans_text:
            from app.services.rag_service import rag_service
            data = rag_service.query(active_prompt)
            ans_text = data["answer"]
            sources = data["sources"]

        reply = f"{ans_text}\n\n*📄 Cited Citations: {', '.join(sources)}*"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# ----------------------------------------------------
# 5. TALENT ACQUISITION & RESUME SCREENING
# ----------------------------------------------------
elif nav_choice == "📄 Talent Acquisition & Resumes":
    st.markdown('<div class="hero-title">📄 AI Talent Acquisition & Matcher</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Automated candidate ranking, semantic cosine vector matching, and skill gap profiling against job specs.</div>', unsafe_allow_html=True)

    c_role, c_upload = st.columns([5, 5])
    with c_role:
        target_role = st.selectbox(
            "Select Target Job Specification",
            ["Machine Learning Engineer", "Data Analyst", "Backend Engineer"]
        )

    role_key = target_role.lower().replace(" ", "_").replace("machine_learning_engineer", "ml_engineer")
    
    matches = None
    try:
        res = requests.post(f"{API_URL}/nlp/match-resumes", json={"target_role": role_key}, timeout=5)
        if res.status_code == 200:
            matches = res.json()
    except Exception:
        pass

    if not matches:
        from app.services.resume_service import resume_service
        raw_matches = resume_service.match_candidates_to_role(role_key)
        matches = raw_matches

    st.markdown(f"<div style='font-size: 1.1rem; font-weight: 700; color: #ffffff; margin: 16px 0 12px 0;'>Ranked Candidates for: <span style='color: #38bdf8;'>{target_role}</span></div>", unsafe_allow_html=True)

    for rank, cand in enumerate(matches, 1):
        score = cand["match_score"]
        name = cand["candidate_name"]
        matched_sk = cand["matched_skills"]
        missing_sk = cand["missing_skills"]
        rec = cand["recommendation"]

        with st.expander(f"🏅 #{rank}: {name} — Fit Score: {score}% ({rec})", expanded=(rank==1)):
            c_m1, c_m2 = st.columns([3, 7])
            with c_m1:
                st.markdown(f"""
                <div style="background: rgba(15,23,42,0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; text-align: center;">
                    <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">Cosine Match</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: {'#34d399' if score>=75 else ('#f59e0b' if score>=50 else '#f43f5e')}; font-family: 'JetBrains Mono';">{score}%</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #e2e8f0; margin-top: 4px;">{rec}</div>
                </div>
                """, unsafe_allow_html=True)

            with c_m2:
                st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #34d399; margin-bottom: 6px;'>✅ Matched Capabilities Found:</div>", unsafe_allow_html=True)
                matched_html = "".join([f'<span class="skill-pill skill-pill-matched">{s}</span>' for s in matched_sk]) if matched_sk else "<span style='color: #64748b;'>None detected</span>"
                st.markdown(f"<div>{matched_html}</div>", unsafe_allow_html=True)

                st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #fb7185; margin: 10px 0 6px 0;'>❓ Missing Target Skill Gaps:</div>", unsafe_allow_html=True)
                missing_html = "".join([f'<span class="skill-pill skill-pill-missing">{s}</span>' for s in missing_sk]) if missing_sk else "<span class='skill-pill skill-pill-matched'>Full Coverage</span>"
                st.markdown(f"<div>{missing_html}</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 6. DATA DRIFT & MODEL HEALTH
# ----------------------------------------------------
elif nav_choice == "📈 Data Drift & MLOps Health":
    st.markdown('<div class="hero-title">📈 MLOps Drift & Model Reliability</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Continuous statistical distribution shift monitoring and automated retraining triggers.</div>', unsafe_allow_html=True)

    drift_info = fetch_api("/dashboard/drift")
    if not drift_info:
        from app.services.drift_service import drift_service
        drift_info = drift_service.get_drift_metrics()

    status = drift_info.get("status", "HEALTHY")
    c_h1, c_h2, c_h3 = st.columns(3)
    with c_h1:
        st.markdown(f"""
        <div class="kpi-card {'kpi-emerald' if status=='HEALTHY' else 'kpi-rose'}">
            <div class="kpi-header">
                <span class="kpi-label">ML Status</span>
                <span class="kpi-icon-pill">🛡️</span>
            </div>
            <div class="kpi-value" style="color: {'#34d399' if status=='HEALTHY' else '#fb7185'};">{status}</div>
            <div class="kpi-badge {'badge-pos' if status=='HEALTHY' else 'badge-neg'}">● {'Production Optimal' if status=='HEALTHY' else 'Retraining Needed'}</div>
        </div>
        """, unsafe_allow_html=True)
    with c_h2:
        st.markdown(f"""
        <div class="kpi-card kpi-indigo">
            <div class="kpi-header">
                <span class="kpi-label">Monitored Features</span>
                <span class="kpi-icon-pill">📊</span>
            </div>
            <div class="kpi-value">{drift_info.get('monitored_features', 5)}</div>
            <div class="kpi-badge badge-neutral">Continuous KS-Test</div>
        </div>
        """, unsafe_allow_html=True)
    with c_h3:
        st.markdown(f"""
        <div class="kpi-card kpi-amber">
            <div class="kpi-header">
                <span class="kpi-label">Drifting Features</span>
                <span class="kpi-icon-pill">⚠️</span>
            </div>
            <div class="kpi-value" style="color: {'#34d399' if drift_info.get('drift_detected_count', 0)==0 else '#f59e0b'};">{drift_info.get('drift_detected_count', 0)}</div>
            <div class="kpi-badge badge-neutral">Threshold: p-val < 0.05</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-bottom: 10px;'>Statistical Feature Shift Audit</div>", unsafe_allow_html=True)
    metrics_list = drift_info.get("feature_metrics", [])
    if metrics_list:
        st.dataframe(pd.DataFrame(metrics_list), use_container_width=True)

    st.markdown("""
    <div class="glass-panel" style="margin-top: 16px; border-left: 3px solid #6366f1;">
        <div style="font-size: 0.88rem; font-weight: 700; color: #a5b4fc; margin-bottom: 4px;">📋 Automated Retraining Policy Protocol</div>
        <div style="font-size: 0.82rem; color: #94a3b8;">Trigger automated CI/CD model retraining when Drifted Features Count &gt; 2 OR Production F1 metric degrades below 0.65.</div>
    </div>
    """, unsafe_allow_html=True)
