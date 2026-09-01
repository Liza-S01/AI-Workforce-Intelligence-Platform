import os
import pandas as pd
from app.utils.config import PROCESSED_DATA_DIR
from app.services.skill_gap_service import skill_gap_service

class RecommendationService:
    def __init__(self):
        self.courses_path = os.path.join(PROCESSED_DATA_DIR, "courses.csv")
        self.emp_path = os.path.join(PROCESSED_DATA_DIR, "employees.csv")

    def _get_courses(self) -> pd.DataFrame:
        if os.path.exists(self.courses_path):
            return pd.read_csv(self.courses_path)
        return pd.DataFrame()

    def get_course_recommendations_for_skills(self, missing_skills: list) -> list:
        courses_df = self._get_courses()
        recs = []
        
        for skill in missing_skills:
            if not courses_df.empty:
                match = courses_df[courses_df["TargetSkill"].str.lower() == skill.lower()]
                if not match.empty:
                    row = match.iloc[0]
                    recs.append({
                        "skill": skill,
                        "course_id": row["CourseID"],
                        "course_title": row["CourseTitle"],
                        "provider": row["Provider"],
                        "duration_hours": int(row["DurationHours"]),
                        "level": row["Level"]
                    })
                    continue
            # Default fallback
            recs.append({
                "skill": skill,
                "course_id": f"CRS-{abs(hash(skill)) % 900 + 100}",
                "course_title": f"Applied Professional Mastery: {skill}",
                "provider": "Enterprise Academy",
                "duration_hours": 16,
                "level": "Intermediate"
            })
        return recs

    def get_workforce_recommendations(self, limit: int = 50) -> list:
        emp_df = pd.read_csv(self.emp_path) if os.path.exists(self.emp_path) else pd.DataFrame()
        if emp_df.empty:
            return []

        results = []
        sample_emps = emp_df.head(limit)
        
        for _, emp in sample_emps.iterrows():
            eid = int(emp["EmployeeID"])
            profile = skill_gap_service.get_employee_skill_profile(eid)
            missing = profile.get("MissingSkills", [])
            course_recs = self.get_course_recommendations_for_skills(missing)
            
            top_rec = course_recs[0]["course_title"] if course_recs else "Continuous Learning Track"
            
            results.append({
                "employee_id": eid,
                "department": emp["Department"],
                "role": emp["JobRole"],
                "missing_skills": missing,
                "top_recommendation": top_rec,
                "courses": course_recs
            })
            
        return results

recommendation_service = RecommendationService()
