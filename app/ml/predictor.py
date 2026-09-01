import os
import csv
from datetime import datetime
import pandas as pd
from app.ml.model_loader import model_loader
from app.ml.explainer import explainer
from app.utils.config import PREDICTIONS_DIR, RISK_THRESHOLDS
from app.utils.logger import logger
from app.validation.employee_schema import EmployeePredictRequest, EmployeePredictResponse

class AttritionPredictor:
    def __init__(self):
        self.prediction_log_path = os.path.join(PREDICTIONS_DIR, "prediction_audit.csv")
        self._init_audit_log()

    def _init_audit_log(self):
        if not os.path.exists(self.prediction_log_path):
            with open(self.prediction_log_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "EmployeeID", "ModelVersion", "Probability", "RiskLevel", "Department", "JobRole"])

    def predict(self, req: EmployeePredictRequest) -> EmployeePredictResponse:
        data_dict = req.model_dump()
        df_input = pd.DataFrame([data_dict])
        
        # Feature Engineering consistent with training
        df_input["TenureRatio"] = df_input["YearsAtCompany"] / (df_input["TotalWorkingYears"] + 1)
        df_input["SatisfactionComposite"] = (
            df_input.get("JobSatisfaction", 3) + 
            df_input.get("EnvironmentSatisfaction", 3) + 
            df_input.get("RelationshipSatisfaction", 3)
        ) / 3.0
        df_input["IncomePerYear"] = df_input["MonthlyIncome"] / (df_input["TotalWorkingYears"] + 1)
        df_input["PromotionGap"] = df_input.get("YearsSinceLastPromotion", 0) / (df_input["YearsInCurrentRole"] + 1)
        
        pipe_data = model_loader.pipeline_data
        version = model_loader.metadata.get("version", "v1.0") if model_loader.metadata else "v1.0"
        
        if pipe_data and "pipeline" in pipe_data:
            pipeline = pipe_data["pipeline"]
            try:
                prob = float(pipeline.predict_proba(df_input)[:, 1][0])
            except Exception as e:
                logger.error(f"Inference error: {e}. Falling back to rule-based risk estimate.")
                prob = self._heuristic_risk(data_dict)
        else:
            prob = self._heuristic_risk(data_dict)
            
        # Determine risk level
        if prob >= RISK_THRESHOLDS["HIGH"]:
            risk_level = "HIGH"
        elif prob >= RISK_THRESHOLDS["MEDIUM"]:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        factors = explainer.explain_instance(data_dict)
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log prediction to audit file
        try:
            with open(self.prediction_log_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([now_str, req.EmployeeID, version, round(prob, 4), risk_level, req.Department, req.JobRole])
        except Exception as e:
            logger.error(f"Failed to write prediction audit log: {e}")
            
        return EmployeePredictResponse(
            EmployeeID=req.EmployeeID,
            AttritionProbability=round(prob, 4),
            RiskLevel=risk_level,
            TopContributingFactors=factors,
            ModelVersion=version,
            Timestamp=now_str
        )

    def _heuristic_risk(self, d: dict) -> float:
        risk = 0.15
        if str(d.get("OverTime", "")).lower() == "yes":
            risk += 0.35
        if d.get("JobSatisfaction", 3) <= 2:
            risk += 0.20
        if d.get("MonthlyIncome", 5000) < 3500:
            risk += 0.15
        if d.get("YearsAtCompany", 5) < 2:
            risk += 0.10
        return min(0.95, risk)

predictor = AttritionPredictor()
