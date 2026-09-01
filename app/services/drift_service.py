import os
import pandas as pd
import numpy as np
from app.utils.config import PROCESSED_DATA_DIR

class DriftService:
    def __init__(self):
        self.emp_path = os.path.join(PROCESSED_DATA_DIR, "employees.csv")

    def get_drift_metrics(self) -> dict:
        if not os.path.exists(self.emp_path):
            return {}

        df = pd.read_csv(self.emp_path)
        
        # Split into reference (first 70%) vs current production (remaining 30%)
        n = len(df)
        split = int(n * 0.7)
        ref_df = df.iloc[:split]
        curr_df = df.iloc[split:]

        features = ["Age", "MonthlyIncome", "YearsAtCompany", "JobSatisfaction", "WorkLifeBalance"]
        drift_report = []

        for feat in features:
            if feat in df.columns:
                ref_mean = float(ref_df[feat].mean())
                ref_std = float(ref_df[feat].std())
                curr_mean = float(curr_df[feat].mean())
                curr_std = float(curr_df[feat].std())

                # Normalized difference
                shift_pct = round(abs(curr_mean - ref_mean) / max(0.001, ref_mean) * 100, 2)
                drift_detected = shift_pct > 15.0

                drift_report.append({
                    "feature": feat,
                    "baseline_mean": round(ref_mean, 2),
                    "current_mean": round(curr_mean, 2),
                    "shift_percentage": shift_pct,
                    "drift_status": "DRIFT DETECTED" if drift_detected else "STABLE"
                })

        return {
            "monitored_features": len(drift_report),
            "drift_detected_count": sum(1 for r in drift_report if r["drift_status"] == "DRIFT DETECTED"),
            "status": "HEALTHY" if sum(1 for r in drift_report if r["drift_status"] == "DRIFT DETECTED") == 0 else "WARNING",
            "feature_metrics": drift_report
        }

drift_service = DriftService()
