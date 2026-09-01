import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.utils.logger import logger
from app.api.attrition import router as attrition_router
from app.api.dashboard import router as dashboard_router
from app.api.skills import router as skills_router
from app.api.nlp_rag import router as rag_router
from app.api.resume_matching import router as resume_router
from app.agents.orchestrator import orchestrator
from app.services.skill_gap_service import skill_gap_service
from app.services.recommendation_service import recommendation_service

app = FastAPI(
    title="AI-Powered Workforce Intelligence Platform",
    description="Agentic HR Intelligence API covering Attrition Risk ML, Skill Gap Engine, Upskilling Pathways, Policy RAG, Resume Screening, and Autonomous Intent Routing.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} ({duration:.3f}s)")
    return response

# Direct Core Endpoint for Employee Profile
@app.get("/employees/{employee_id}", tags=["Core Employees"])
def get_employee_intelligence_record(employee_id: int):
    """
    Returns full intelligence record for one employee (role, skills, gap, courses).
    """
    profile = skill_gap_service.get_employee_skill_profile(employee_id)
    if not profile:
        return {"error": f"Employee {employee_id} not found"}
    courses = recommendation_service.get_course_recommendations_for_skills(profile.get("MissingSkills", []))
    profile["RecommendedCourses"] = courses
    return profile

# Agentic Orchestration Endpoint (Phase 7)
class AgentQueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None

@app.post("/agent/query", tags=["Agentic Orchestrator"])
def query_agent_orchestrator(req: AgentQueryRequest):
    """
    Autonomous multi-agent routing layer: classifies query intent and dispatches to specialized agent.
    """
    return orchestrator.execute(req.query, req.context)

# Register API Routers
app.include_router(attrition_router)
app.include_router(dashboard_router)
app.include_router(skills_router)
app.include_router(rag_router)
app.include_router(resume_router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "platform": "AI-Powered Workforce Intelligence Platform",
        "version": "v1.1.0",
        "docs_url": "/docs",
        "services": [
            "Agentic Orchestrator (Intent-driven routing)",
            "Attrition Risk ML Engine (XGBoost / Gradient Boosting / SHAP)",
            "Organization Skill Gap Engine",
            "Upskilling Recommendation Engine",
            "HR Policy RAG Q&A",
            "Resume-to-Job Matcher",
            "MLOps Data Drift Monitor"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
