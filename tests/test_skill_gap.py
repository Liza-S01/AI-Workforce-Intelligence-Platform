from app.services.skill_gap_service import skill_gap_service
from app.services.recommendation_service import recommendation_service

def test_organization_skill_gaps_retrieval():
    gaps = skill_gap_service.get_organization_skill_gaps()
    assert isinstance(gaps, list)
    if gaps:
        first = gaps[0]
        assert "skill" in first
        assert "employees_missing" in first
        assert "severity" in first
        assert first["severity"] in ["HIGH", "MEDIUM", "LOW"]

def test_course_recommendations():
    missing = ["MLOps", "Docker", "Python"]
    courses = recommendation_service.get_course_recommendations_for_skills(missing)
    assert len(courses) == 3
    assert all("course_title" in c for c in courses)
    assert all("provider" in c for c in courses)
