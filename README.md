# AI-Powered Workforce Intelligence Platform

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-teal.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4.0-orange.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/pytest-14%20passed-brightgreen.svg)](https://pytest.org/)

An enterprise-grade, full-stack workforce intelligence and upskilling platform that predicts employee attrition risk, detects and closes organization-wide skill gaps, answers HR policy questions via RAG, screens candidate resumes, and orchestrates tasks with an autonomous multi-agent routing layer.

---

## 📢 Real vs. Synthetic Data Disclosure

This project adheres strictly to clear data provenance rules as documented in [**`data/SYNTHETIC_DATA_NOTE.md`**](file:///d:/Agentic-HR-Project/data/SYNTHETIC_DATA_NOTE.md):
- **5 Real Foundational Datasets** (in `data/raw/`): `employee_attrition.csv` (IBM HR), `hr_performance_engagement.csv`, `occupation_data.csv` (O*NET), `essential_skills.csv` (O*NET), `software_skills.csv` (O*NET).
- **Synthetic Simulated Artifacts**: `employee_skills.csv`, `courses.csv`, HR Policy PDFs (Leave, Remote Work, Payroll, Learning), Candidate Resumes, and Job Descriptions.

---

## 🏛️ System Architecture & Multi-Agent Routing

```
┌────────────────────────────────────────────────────────┐
│                   HR DATA SOURCES                      │
│     5 Real Datasets (IBM / ONET) + Synthetic Data      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                 DATA INGESTION LAYER                   │
│         CSV / PDF Validation, Cleaning & ETL           │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               CENTRAL HR DATA PLATFORM                 │
│         Processed CSVs & Serialized Ontologies         │
└───────────────────────────┬────────────────────────────┘
                            │
      ┌─────────────────────┼─────────────────────┐
      │                     │                     │
      ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  ML ENGINE   │     │ AI / NLP     │     │ BUSINESS     │
│              │     │ ENGINE       │     │ ENGINE       │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
 Attrition Risk       RAG Policy QA        Skill Gap
 Probability & SHAP   Resume Screening     Upskilling Pathways
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│           AGENTIC ORCHESTRATOR (Phase 7)               │
│          Intent Classification & Dispatch              │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                  SERVICE / API LAYER                   │
│                        FastAPI                         │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                 FRONTEND / DASHBOARD                   │
│                       Streamlit                        │
└────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
Agentic-HR-Project/
├── data/
│   ├── raw/                           # 5 Real Datasets, untouched
│   │   ├── employee_attrition.csv
│   │   ├── hr_performance_engagement.csv
│   │   ├── occupation_data.csv
│   │   ├── essential_skills.csv
│   │   └── software_skills.csv
│   ├── processed/                     # Cleaned, standardized tables
│   │   ├── employees.csv
│   │   ├── employee_skills.csv
│   │   ├── role_skills.csv
│   │   ├── courses.csv
│   │   ├── performance_history.csv
│   │   └── engagement_data.csv
│   ├── hr_policies/                   # Synthetic policy PDFs
│   │   ├── leave_policy.pdf
│   │   ├── remote_work_policy.pdf
│   │   ├── payroll_policy.pdf
│   │   └── learning_policy.pdf
│   ├── resumes/                       # Synthetic candidate resumes (PDF + text)
│   │   ├── candidate_001.pdf
│   │   ├── candidate_002.pdf
│   │   └── candidate_003.pdf
│   ├── job_descriptions/              # Standardized JDs
│   │   ├── ml_engineer.txt
│   │   ├── data_analyst.txt
│   │   └── backend_engineer.txt
│   ├── predictions/                   # Prediction audit history
│   └── SYNTHETIC_DATA_NOTE.md         # Explicit data provenance disclosure
│
├── notebooks/                         # 01–16 Numbered Jupyter notebooks
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_validation.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_data_relationships.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_baseline_model.ipynb
│   ├── 07_model_comparison.ipynb
│   ├── 08_model_explainability.ipynb
│   ├── 09_model_versioning.ipynb
│   ├── 10_engagement_intelligence.ipynb
│   ├── 11_role_intelligence.ipynb
│   ├── 12_employee_skills.ipynb
│   ├── 13_skill_gap_engine.ipynb
│   ├── 14_organization_skill_gap.ipynb
│   ├── 15_recommendation_engine.ipynb
│   └── 16_employee_intelligence.ipynb
│
├── models/
│   └── v1/
│       ├── attrition_pipeline.joblib  # Serialized ML pipeline
│       └── metadata.json              # Version metadata & thresholds
│
├── app/
│   ├── main.py                        # FastAPI entrypoint
│   ├── api/                           # REST API routes
│   │   ├── attrition.py
│   │   ├── dashboard.py
│   │   ├── skills.py
│   │   ├── nlp_rag.py
│   │   └── resume_matching.py
│   ├── services/                      # Core business logic & engines
│   │   ├── attrition_service.py
│   │   ├── engagement_service.py
│   │   ├── skill_gap_service.py
│   │   ├── recommendation_service.py
│   │   ├── rag_service.py
│   │   ├── resume_service.py
│   │   └── drift_service.py
│   ├── validation/                    # Pydantic schemas
│   │   ├── employee_schema.py
│   │   └── engagement_schema.py
│   ├── ml/                            # Model loaders & predictors
│   │   ├── model_loader.py
│   │   ├── predictor.py
│   │   └── explainer.py
│   ├── agents/                        # Phase 7 Agentic Routing Layer
│   │   └── orchestrator.py
│   └── utils/
│       ├── config.py
│       └── logger.py
│
├── frontend/
│   └── app.py                         # Streamlit interactive dashboard
│
├── tests/                             # Automated test suite (Pytest)
│   ├── test_validation.py
│   ├── test_attrition_model.py
│   ├── test_skill_gap.py
│   └── test_api.py
│
├── scripts/
│   ├── setup_data.py
│   ├── train_model.py
│   ├── generate_notebooks.py
│   └── superstore_eda.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🚀 Quickstart Guide

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run Automated Unit Tests
```bash
python -m pytest -v
```

### 3. Start Backend & Frontend
- **FastAPI Backend**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```
  *(Interactive Swagger API docs at [http://localhost:8000/docs](http://localhost:8000/docs))*

- **Streamlit Executive Dashboard**:
  ```bash
  streamlit run frontend/app.py
  ```
  *(Dashboard UI at [http://localhost:8501](http://localhost:8501))*

  ## 🌐 Live Cloud Demo
- 🚀 **Live Interactive App (Streamlit)**: [https://ai-workforce-intelligence-platform-mdzvd4wsmuuxesqh2xbaoy.streamlit.app/](https://ai-workforce-intelligence-platform-mdzvd4wsmuuxesqh2xbaoy.streamlit.app/)
- ⚡ **Live Backend Swagger API (Render)**: [https://hr-ai-backend-cuuc.onrender.com](https://hr-ai-backend-cuuc.onrender.com)

