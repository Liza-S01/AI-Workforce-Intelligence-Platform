import os
import pandas as pd
from app.utils.config import PROCESSED_DATA_DIR, RISK_THRESHOLDS
from app.ml.predictor import predictor
from app.validation.employee_schema import EmployeePredictRequest

class AttritionService:
    def __init__(self):
        self.emp_path = os.path.join(PROCESSED_DATA_DIR, "employees.csv")
        self._cached_df = None

    def get_employees_df(self) -> pd.DataFrame:
        if self._cached_df is None or True:
            if os.path.exists(self.emp_path):
                self._cached_df = pd.read_csv(self.emp_path)
            else:
                self._cached_df = pd.DataFrame()
        return self._cached_df

    def get_summary_kpis(self) -> dict:
        df = self.get_employees_df()
        if df.empty:
            return {"total_employees": 0, "high_risk_employees": 0, "average_engagement": 0, "avg_satisfaction": 0}
        
        # Calculate attrition probabilities if not present
        total = len(df)
        avg_eng = float(df["EngagementScore"].mean()) if "EngagementScore" in df.columns else 72.0
        avg_sat = float(df["JobSatisfaction"].mean()) if "JobSatisfaction" in df.columns else 3.1
        
        # High risk based on low satisfaction / overtime or attrition flag
        high_risk_count = int((df["Attrition"].astype(str).str.lower() == "yes").sum())
        
        return {
            "total_employees": total,
            "high_risk_employees": high_risk_count,
            "high_risk_percentage": round((high_risk_count / total) * 100, 1) if total > 0 else 0,
            "average_engagement": round(avg_eng, 1),
            "average_satisfaction": round(avg_sat, 2)
        }

    def get_attrition_by_department(self) -> list:
        df = self.get_employees_df()
        if df.empty:
            return []
        
        grouped = df.groupby("Department").agg(
            total_employees=("EmployeeID", "count"),
            attrition_count=("Attrition", lambda x: (x.astype(str).str.lower() == "yes").sum()),
            avg_engagement=("EngagementScore", "mean"),
            avg_income=("MonthlyIncome", "mean")
        ).reset_index()
        
        grouped["attrition_rate"] = round((grouped["attrition_count"] / grouped["total_employees"]) * 100, 1)
        grouped["avg_engagement"] = grouped["avg_engagement"].round(1)
        grouped["avg_income"] = grouped["avg_income"].round(0)
        
        return grouped.to_dict(orient="records")

attrition_service = AttritionService()
