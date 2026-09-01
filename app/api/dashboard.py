from fastapi import APIRouter, HTTPException
from app.services.attrition_service import attrition_service
from app.services.engagement_service import engagement_service
from app.services.skill_gap_service import skill_gap_service
from app.services.recommendation_service import recommendation_service
from app.services.drift_service import drift_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard & Analytics"])

@router.get("/summary")
def get_dashboard_summary():
    """
    Returns core workforce KPI cards (Total Employees, High Risk, Avg Engagement, Satisfaction).
    """
    return attrition_service.get_summary_kpis()

@router.get("/attrition-by-department")
def get_department_attrition():
    """
    Returns department-level workforce breakdown and attrition risk rates.
    """
    return attrition_service.get_attrition_by_department()

@router.get("/skill-gaps")
def get_org_skill_gaps():
    """
    Returns organization-wide missing skills ranked by severity.
    """
    return skill_gap_service.get_organization_skill_gaps()

@router.get("/recommendations")
def get_workforce_recommendations(limit: int = 50):
    """
    Returns employee upskilling course pathways.
    """
    return recommendation_service.get_workforce_recommendations(limit=limit)

@router.get("/engagement")
def get_engagement_analytics():
    """
    Returns engagement distribution and low-engagement alerts.
    """
    return engagement_service.get_engagement_metrics()

@router.get("/drift")
def get_data_drift():
    """
    Returns data distribution drift statistics for production monitoring.
    """
    return drift_service.get_drift_metrics()
