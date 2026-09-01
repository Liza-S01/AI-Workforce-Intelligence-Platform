import os
import pandas as pd
from app.utils.config import PROCESSED_DATA_DIR

class SkillGapService:
    def __init__(self):
        self.emp_path = os.path.join(PROCESSED_DATA_DIR, "employees.csv")
        self.role_path = os.path.join(PROCESSED_DATA_DIR, "role_skills.csv")
        self.skill_path = os.path.join(PROCESSED_DATA_DIR, "employee_skills.csv")

    def _load_data(self):
        emp_df = pd.read_csv(self.emp_path) if os.path.exists(self.emp_path) else pd.DataFrame()
        role_df = pd.read_csv(self.role_path) if os.path.exists(self.role_path) else pd.DataFrame()
        skill_df = pd.read_csv(self.skill_path) if os.path.exists(self.skill_path) else pd.DataFrame()
        return emp_df, role_df, skill_df

    def get_organization_skill_gaps(self) -> list:
        emp_df, role_df, skill_df = self._load_data()
        if emp_df.empty or role_df.empty or skill_df.empty:
            return []

        # Role to required skills mapping
        role_map = {}
        for _, r in role_df.iterrows():
            role_map[r["JobRole"]] = [s.strip() for s in r["RequiredSkills"].split(",")]

        # Employee to held skills mapping
        emp_skills_map = skill_df.groupby("EmployeeID")["Skill"].apply(lambda s: set(s.str.lower())).to_dict()

        gap_counts = {}
        domain_map = {r["JobRole"]: r.get("Domain", "General") for _, r in role_df.iterrows()}
        skill_domains = {}

        for _, emp in emp_df.iterrows():
            eid = emp["EmployeeID"]
            role = emp["JobRole"]
            req = role_map.get(role, [])
            has = emp_skills_map.get(eid, set())
            
            for s in req:
                s_clean = s.strip()
                if s_clean.lower() not in has:
                    gap_counts[s_clean] = gap_counts.get(s_clean, 0) + 1
                    skill_domains[s_clean] = domain_map.get(role, "General")

        gaps = []
        for skill, count in sorted(gap_counts.items(), key=lambda x: x[1], reverse=True):
            if count >= 150:
                severity = "HIGH"
            elif count >= 80:
                severity = "MEDIUM"
            else:
                severity = "LOW"
                
            gaps.append({
                "skill": skill,
                "employees_missing": count,
                "severity": severity,
                "domain": skill_domains.get(skill, "General")
            })

        return gaps

    def get_employee_skill_profile(self, employee_id: int) -> dict:
        emp_df, role_df, skill_df = self._load_data()
        emp_match = emp_df[emp_df["EmployeeID"] == employee_id]
        if emp_match.empty:
            return {}

        emp_record = emp_match.iloc[0]
        role = emp_record["JobRole"]
        
        # Required skills for role
        role_match = role_df[role_df["JobRole"] == role]
        req_skills = []
        if not role_match.empty:
            req_skills = [s.strip() for s in role_match.iloc[0]["RequiredSkills"].split(",")]
        else:
            req_skills = ["Communication", "Problem Solving", "Domain Analysis"]

        # Current employee skills
        emp_skills_rows = skill_df[skill_df["EmployeeID"] == employee_id]
        current_skills = emp_skills_rows["Skill"].tolist() if not emp_skills_rows.empty else ["Communication"]
        current_skills_lower = set([s.lower() for s in current_skills])

        # Missing skills
        missing = [s for s in req_skills if s.lower() not in current_skills_lower]

        return {
            "EmployeeID": employee_id,
            "Department": emp_record["Department"],
            "JobRole": role,
            "RequiredSkills": req_skills,
            "CurrentSkills": current_skills,
            "MissingSkills": missing,
            "CoveragePercentage": round((len(req_skills) - len(missing)) / max(1, len(req_skills)) * 100, 1)
        }

skill_gap_service = SkillGapService()
