import os
import pandas as pd
from app.utils.config import PROCESSED_DATA_DIR

class EngagementService:
    def __init__(self):
        self.eng_path = os.path.join(PROCESSED_DATA_DIR, "engagement_data.csv")

    def get_engagement_metrics(self) -> dict:
        if not os.path.exists(self.eng_path):
            return {}
        df = pd.read_csv(self.eng_path)
        
        dept_dist = df.groupby("Department")["EngagementScore"].mean().round(1).to_dict()
        cat_counts = df["EngagementCategory"].value_counts().to_dict() if "EngagementCategory" in df.columns else {}
        
        low_eng_employees = df[df["EngagementScore"] < 50][["EmployeeID", "Department", "JobRole", "EngagementScore"]].head(10).to_dict(orient="records")
        
        return {
            "department_engagement": dept_dist,
            "category_distribution": cat_counts,
            "lowest_engagement_sample": low_eng_employees
        }

engagement_service = EngagementService()
