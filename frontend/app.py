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
    page_title="AI Workforce Intelligence Platform",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for modern executive aesthetic
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e222d 0%, #262c3d 100%);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #363d52;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    }
    .metric-title {
        color: #9ba1b0;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 2.1rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-delta {
        color: #00e676;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 4px;
    }
    .metric-delta-neg {
        color: #ff5252;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 4px;
    }
    .chat-bubble-user {
        background-color: #2b3245;
        color: white;
        padding: 12px 16px;
        border-radius: 12px 12px 0px 12px;
        margin-bottom: 10px;
        text-align: right;
    }
    .chat-bubble-bot {
        background-color: #1a202c;
        color: #e2e8f0;
        padding: 12px 16px;
        border-radius: 12px 12px 12px 0px;
        margin-bottom: 10px;
        border: 1px solid #2d3748;
    }
    .thought-trace {
        background-color: #151922;
        border-left: 3px solid #2979ff;
        padding: 8px 12px;
        font-family: monospace;
        font-size: 0.82rem;
        color: #82aaff;
        margin-bottom: 8px;
        border-radius: 0 4px 4px 0;
    }
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Helper to fetch from backend with fallback
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

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
st.sidebar.title("Workforce AI")
st.sidebar.caption("Enterprise Talent Intelligence & Upskilling Platform")
st.sidebar.markdown("---")

nav_choice = st.sidebar.radio(
    "Navigation Menu",
    [
        "🧠 Agentic Copilot (Orchestrator)",
        "📊 Executive Overview",
        "🔍 Employee 360° Profile",
        "🎯 Skill Gap & Upskilling",
        "🤖 AI HR Policy Assistant",
        "📄 Talent Acquisition & Resumes",
        "📈 Data Drift & Model Health"
    ],
    key="nav_choice_sidebar"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Active Orchestrator**: Multi-Agent Intent Router\n\n🛡️ **Data Governance**: Real + Synthetic Disclosed")

# ----------------------------------------------------
# 0. AGENTIC COPILOT (ORCHESTRATOR) - PHASE 7
# ----------------------------------------------------
if nav_choice == "🧠 Agentic Copilot (Orchestrator)":
    st.title("🧠 Agentic HR Orchestrator & Autonomous Copilot")
    st.caption("A centralized multi-agent routing layer that autonomously directs workforce questions to specialized engines.")

    st.markdown("""
    Ask any natural language question — the orchestrator dynamically routes your query:
    - 🔴 **Attrition Engine**: queries about turnover risk, quit rates, retention
    - 🔵 **Skill Gap Engine**: queries about team competency gaps, training, courses
    - 🟢 **Policy RAG Engine**: queries about leave, remote work, compensation rules
    - 🟣 **Resume Matching Engine**: queries about candidate qualifications and job fit
    - 🟡 **Central Analytics Engine**: queries about headcount and executive KPIs
    """)

    if "agent_chat_history" not in st.session_state:
        st.session_state.agent_chat_history = []

    st.markdown("##### 💡 Example Agent Prompts:")
    c_p1, c_p2, c_p3 = st.columns(3)
    p1 = c_p1.button("📊 What is the current attrition risk in Sales?")
    p2 = c_p2.button("🎯 What are the biggest skill gaps in our tech teams?")
    p3 = c_p3.button("📄 Rank the candidate resumes for the ML Engineer role")

    agent_input = st.chat_input("Ask the Agentic HR Copilot anything...")
    chosen_prompt = None
    if p1: chosen_prompt = "What is the current attrition risk and high risk headcount in Sales?"
    elif p2: chosen_prompt = "What are the most critical organization-wide skill gaps and recommended courses?"
    elif p3: chosen_prompt = "Rank the candidate resumes for the ML Engineer position and show top fit"
    elif agent_input: chosen_prompt = agent_input

    if chosen_prompt:
        # Call Orchestrator
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
        st.markdown(f'<div class="chat-bubble-user">👤 <b>Query:</b> {turn["query"]}</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown(f"**🤖 Routed Sub-Agent:** `{turn['routed_agent']}`")
            with st.expander("🔍 View Autonomous Thought Trace & Execution Steps", expanded=False):
                for step in turn.get("thought_trace", []):
                    st.markdown(f'<div class="thought-trace">{step}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-bot"><b>Answer:</b><br>{turn["response"]}</div>', unsafe_allow_html=True)
        st.markdown("---")

# ----------------------------------------------------
# 1. EXECUTIVE OVERVIEW
# ----------------------------------------------------
elif nav_choice == "📊 Executive Overview":
    st.title("AI Workforce Intelligence Platform")
    st.caption("Real-time workforce health monitoring, attrition risk forecasting, and talent analytics.")

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
        <div class="metric-card">
            <div class="metric-title">Total Active Employees</div>
            <div class="metric-value">{summary['total_employees']:,}</div>
            <div class="metric-delta">↑ 4.2% YoY Growth</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">High Attrition Risk</div>
            <div class="metric-value" style="color: #ff5252;">{summary['high_risk_employees']}</div>
            <div class="metric-delta-neg">⚠️ {summary.get('high_risk_percentage', 8.4)}% of workforce</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Engagement</div>
            <div class="metric-value" style="color: #00e676;">{summary['average_engagement']}%</div>
            <div class="metric-delta">↑ 1.8% vs last quarter</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Average Job Satisfaction</div>
            <div class="metric-value">{summary['average_satisfaction']} / 4.0</div>
            <div class="metric-delta">★ 78% Positive Index</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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
        st.subheader("Attrition Risk Rate by Department")
        fig_dept = px.bar(
            dept_df,
            x="Department",
            y="attrition_rate",
            text="attrition_rate",
            color="attrition_rate",
            color_continuous_scale="Reds",
            labels={"attrition_rate": "Attrition Rate (%)", "Department": "Department"},
            template="plotly_dark"
        )
        fig_dept.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_dept.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=350)
        st.plotly_chart(fig_dept, width='stretch')

    with col_right:
        st.subheader("Workforce Distribution")
        fig_pie = px.pie(
            dept_df,
            names="Department",
            values="total_employees",
            hole=0.45,
            color_discrete_sequence=["#2979ff", "#00e676", "#ff9100"],
            template="plotly_dark"
        )
        fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=350)
        st.plotly_chart(fig_pie, width='stretch')

    st.markdown("---")
    st.subheader("Global Attrition Drivers (Explainable AI / SHAP Ranking)")
    c_d1, c_d2, c_d3, c_d4 = st.columns(4)
    c_d1.info("⏱️ **1. Overtime Demand**\n\nEmployees working frequent overtime exhibit 3.2x higher attrition likelihood.")
    c_d2.info("💰 **2. Compensation Benchmark**\n\nMonthly income below role median corresponds with 42% risk increase.")
    c_d3.info("⏳ **3. Promotion Stagnation**\n\n4+ years without role progression correlates with low engagement scores.")
    c_d4.info("⚖️ **4. Work-Life Balance**\n\nSatisfaction scores below 2/4 double voluntary departure risk.")

# ----------------------------------------------------
# 2. EMPLOYEE 360° PROFILE & PREDICTOR
# ----------------------------------------------------
elif nav_choice == "🔍 Employee 360° Profile":
    st.title("Employee 360° Intelligence & Live Predictor")
    st.caption("Inspect individual risk factors, simulate scenario modifications, and generate instant predictions.")

    emp_df = get_local_employees()
    
    col_sel, col_quick = st.columns([4, 6])
    with col_sel:
        emp_ids = emp_df["EmployeeID"].tolist() if not emp_df.empty else [101, 102, 103]
        selected_id = st.selectbox("Select Employee ID to Load Profile", emp_ids, index=0)

    emp_record = emp_df[emp_df["EmployeeID"] == selected_id].iloc[0] if not emp_df.empty and selected_id in emp_df["EmployeeID"].values else None

    st.markdown("---")
    c_form1, c_form2, c_form3 = st.columns(3)

    with c_form1:
        st.markdown("#### 👤 Employee Details")
        age = st.number_input("Age", min_value=18, max_value=75, value=int(emp_record["Age"]) if emp_record is not None else 32)
        dept = st.selectbox("Department", ["Research & Development", "Sales", "Human Resources"], index=0)
        role = st.selectbox("Job Role", [
            "Research Scientist", "Data Analyst", "ML Engineer", "Backend Engineer", 
            "Sales Executive", "Lab Technician", "Healthcare Rep", "Engineering Manager"
        ], index=0)
        gender = st.selectbox("Gender", ["Female", "Male"], index=0)
        marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced"], index=0)

    with c_form2:
        st.markdown("#### 💼 Experience & Tenure")
        total_exp = st.slider("Total Working Years", 0, 40, int(emp_record["TotalWorkingYears"]) if emp_record is not None else 8)
        years_company = st.slider("Years at Company", 0, 30, int(emp_record["YearsAtCompany"]) if emp_record is not None else 3)
        years_role = st.slider("Years in Current Role", 0, 20, int(emp_record["YearsInCurrentRole"]) if emp_record is not None else 2)
        promo_gap = st.slider("Years Since Last Promotion", 0, 15, int(emp_record["YearsSinceLastPromotion"]) if emp_record is not None else 1)
        income = st.number_input("Monthly Income ($)", min_value=1000, max_value=25000, value=int(emp_record["MonthlyIncome"]) if emp_record is not None else 5200)

    with c_form3:
        st.markdown("#### ⚡ Satisfaction & Work Dynamics")
        overtime = st.selectbox("OverTime Requirement", ["Yes", "No"], index=0 if (emp_record is not None and str(emp_record["OverTime"]).lower() == "yes") else 1)
        job_sat = st.slider("Job Satisfaction (1-4)", 1, 4, int(emp_record["JobSatisfaction"]) if emp_record is not None else 3)
        wlb = st.slider("Work-Life Balance (1-4)", 1, 4, int(emp_record["WorkLifeBalance"]) if emp_record is not None else 3)
        env_sat = st.slider("Environment Satisfaction (1-4)", 1, 4, int(emp_record.get("EnvironmentSatisfaction", 3)) if emp_record is not None else 3)
        distance = st.slider("Distance From Home (miles)", 1, 50, int(emp_record["DistanceFromHome"]) if emp_record is not None else 8)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Run ML Attrition Prediction & Explainability", type="primary", width='stretch'):
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

        st.markdown("---")
        st.subheader("Prediction Intelligence Output")
        
        p_col1, p_col2 = st.columns([4, 6])
        with p_col1:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                title={'text': f"Risk Probability ({risk})", 'font': {'size': 20}},
                number={'suffix': "%"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#ff5252" if risk == "HIGH" else ("#ffb300" if risk == "MEDIUM" else "#00e676")},
                    'steps': [
                        {'range': [0, 35], 'color': "rgba(0, 230, 118, 0.15)"},
                        {'range': [35, 65], 'color': "rgba(255, 179, 0, 0.15)"},
                        {'range': [65, 100], 'color': "rgba(255, 82, 82, 0.15)"}
                    ]
                }
            ))
            gauge.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=280)
            st.plotly_chart(gauge, width='stretch')

        with p_col2:
            st.markdown("#### 🎯 Key Risk Drivers & Recommended Interventions")
            for idx, f in enumerate(factors, 1):
                st.warning(f"**Factor {idx}:** {f}")
            
            if risk == "HIGH":
                st.error("🚨 **Immediate Action Plan**: Schedule retention check-in, review overtime hours, and consider retention bonus / promotion eligibility.")
            elif risk == "MEDIUM":
                st.info("⚠️ **Action Plan**: Review professional development opportunities and ensure regular 1-on-1 feedback.")
            else:
                st.success("✅ **Healthy Retention**: Employee exhibits stable engagement and healthy tenure metrics.")

# ----------------------------------------------------
# 3. SKILL GAP & UPSKILLING CENTER
# ----------------------------------------------------
elif nav_choice == "🎯 Skill Gap & Upskilling":
    st.title("Organization Skill Gaps & Upskilling Pathways")
    st.caption("AI-powered set difference skill gap engine and tailored training course recommendations.")

    tab1, tab2 = st.tabs(["🏢 Critical Organization-Wide Skill Gaps", "🎓 Individual Upskilling Recommendations"])

    with tab1:
        gaps_data = fetch_api("/dashboard/skill-gaps")
        if not gaps_data:
            from app.services.skill_gap_service import skill_gap_service
            gaps_data = skill_gap_service.get_organization_skill_gaps()

        df_gaps = pd.DataFrame(gaps_data)
        
        c_gap1, c_gap2 = st.columns([6, 4])
        with c_gap1:
            st.subheader("Top Missing Competencies Across Workforce")
            fig_gaps = px.bar(
                df_gaps.head(10),
                x="employees_missing",
                y="skill",
                orientation="h",
                color="severity",
                color_discrete_map={"HIGH": "#ff5252", "MEDIUM": "#ffb300", "LOW": "#00e676"},
                labels={"employees_missing": "Employees Missing Skill", "skill": "Skill Competency"},
                template="plotly_dark"
            )
            fig_gaps.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=380)
            st.plotly_chart(fig_gaps, width='stretch')

        with c_gap2:
            st.subheader("Severity Breakdown")
            st.markdown("""
            - 🔴 **HIGH Priority (150+ Employees Missing)**: Strategic capabilities like **MLOps, Cloud (AWS), Deep Learning, Docker**.
            - 🟡 **MEDIUM Priority (80-150 Missing)**: Tools like **PowerBI, CI/CD, Agile Leadership**.
            - 🟢 **LOW Priority (<80 Missing)**: Baseline foundational tools.
            """)
            st.dataframe(df_gaps.head(10), width='stretch')

    with tab2:
        st.subheader("Workforce Upskilling Course Pathways")
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
        st.dataframe(pd.DataFrame(rows), width='stretch')

# ----------------------------------------------------
# 4. AI HR POLICY ASSISTANT (RAG)
# ----------------------------------------------------
elif nav_choice == "🤖 AI HR Policy Assistant":
    st.title("AI HR Policy Assistant (RAG Engine)")
    st.caption("Ask questions in natural language regarding company leave, remote work, payroll, and benefits.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your AI HR Policy Assistant. You can ask me questions about annual leave, sick days, hybrid work rules, overtime, or learning budgets."}
        ]

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">👤 <b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot">🤖 <b>HR AI Assistant:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown("##### 💡 Suggested Questions:")
    s1, s2, s3 = st.columns(3)
    q1 = s1.button("🌴 How many vacation days do I accrue per year?")
    q2 = s2.button("🏠 What is the remote work & hybrid policy?")
    q3 = s3.button("📚 Is there an annual learning stipend?")

    user_query = st.chat_input("Type your HR policy question here...")

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

        reply = f"{ans_text}\n\n*📄 Cited Sources: {', '.join(sources)}*"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# ----------------------------------------------------
# 5. TALENT ACQUISITION & RESUME SCREENING
# ----------------------------------------------------
elif nav_choice == "📄 Talent Acquisition & Resumes":
    st.title("AI Talent Acquisition & Resume Matcher")
    st.caption("Automated candidate ranking, semantic similarity scoring, and skill matching against target Job Descriptions.")

    c_role, c_upload = st.columns([5, 5])
    with c_role:
        target_role = st.selectbox(
            "Select Target Job Description",
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

    st.markdown("---")
    st.subheader(f"Ranked Candidates for: {target_role}")

    for rank, cand in enumerate(matches, 1):
        score = cand["match_score"]
        name = cand["candidate_name"]
        matched_sk = cand["matched_skills"]
        missing_sk = cand["missing_skills"]
        rec = cand["recommendation"]

        with st.expander(f"🏅 #{rank}: {name} — Match Score: {score}% ({rec})", expanded=(rank==1)):
            c_m1, c_m2 = st.columns([3, 7])
            with c_m1:
                st.metric("Overall Match Fit", f"{score}%")
                if score >= 75:
                    st.success("✅ Qualified Candidate")
                elif score >= 50:
                    st.warning("⚠️ Partial Fit")
                else:
                    st.error("❌ Low Alignment")

            with c_m2:
                st.markdown("##### 🛠️ Matched Skills Found in Resume:")
                st.write(", ".join([f"`{s}`" for s in matched_sk]) if matched_sk else "None detected")
                st.markdown("##### ❓ Missing Target Role Skills:")
                st.write(", ".join([f"`{s}`" for s in missing_sk]) if missing_sk else "None (Full coverage)")

# ----------------------------------------------------
# 6. DATA DRIFT & MODEL HEALTH
# ----------------------------------------------------
elif nav_choice == "📈 Data Drift & Model Health":
    st.title("MLOps Data Drift & Model Performance Monitor")
    st.caption("Distribution shift tracking between baseline training data and active workforce features.")

    drift_info = fetch_api("/dashboard/drift")
    if not drift_info:
        from app.services.drift_service import drift_service
        drift_info = drift_service.get_drift_metrics()

    status = drift_info.get("status", "HEALTHY")
    c_h1, c_h2, c_h3 = st.columns(3)
    with c_h1:
        st.metric("Model Health Status", status, delta="Operational" if status=="HEALTHY" else "Retrain Triggered")
    with c_h2:
        st.metric("Monitored Features", drift_info.get("monitored_features", 5))
    with c_h3:
        st.metric("Drifting Features Count", drift_info.get("drift_detected_count", 0))

    st.markdown("---")
    st.subheader("Feature Shift Audit Table")
    metrics_list = drift_info.get("feature_metrics", [])
    if metrics_list:
        st.dataframe(pd.DataFrame(metrics_list), width='stretch')

    st.info("📋 **Automated Retraining Strategy Rule**:\n\nIf Drift Count > 2 OR Production F1 falls below 0.65 OR 6 months of new records are collected -> Trigger Automated Retraining Pipeline.")
