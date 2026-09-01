from fastapi import APIRouter, HTTPException
from app.services.skill_gap_service import skill_gap_service
from app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/skills", tags=["Skill Gap & Upskilling Engine"])

@router.get("/employee/{employee_id}")
def get_employee_skills(employee_id: int):
    """
    Returns 360 degree skill profile, coverage %, and missing skills for an individual employee.
    """
    profile = skill_gap_service.get_employee_skill_profile(employee_id)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Employee ID {employee_id} not found")
    
    # Add course recommendations for missing skills
    courses = recommendation_service.get_course_recommendations_for_skills(profile["MissingSkills"])
    profile["RecommendedCourses"] = courses
    return profile
