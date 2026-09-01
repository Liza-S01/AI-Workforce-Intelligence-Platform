import numpy as np
import pandas as pd
from app.ml.model_loader import model_loader
from app.utils.logger import logger

class ModelExplainer:
    def __init__(self):
        self.top_features_global = [
            "OverTime", "MonthlyIncome", "YearsAtCompany", 
            "JobSatisfaction", "WorkLifeBalance", "DistanceFromHome", "Age"
        ]

    def explain_instance(self, input_dict: dict) -> list:
        reasons = []
        if str(input_dict.get("OverTime", "")).lower() == "yes":
            reasons.append("Frequent Overtime demand increases fatigue risk")
        if input_dict.get("JobSatisfaction", 3) <= 2:
            reasons.append(f"Low Job Satisfaction rating ({input_dict.get('JobSatisfaction')}/4)")
        if input_dict.get("WorkLifeBalance", 3) <= 2:
            reasons.append(f"Challenged Work-Life Balance ({input_dict.get('WorkLifeBalance')}/4)")
        if input_dict.get("MonthlyIncome", 5000) < 3500:
            reasons.append("Compensation below role benchmark")
        if input_dict.get("YearsSinceLastPromotion", 0) >= 4:
            reasons.append(f"Long promotion stagnation ({input_dict.get('YearsSinceLastPromotion')} yrs)")
        if input_dict.get("DistanceFromHome", 5) > 15:
            reasons.append(f"Extended commute distance ({input_dict.get('DistanceFromHome')} miles)")
            
        if not reasons:
            reasons = ["Tenure ratio and market compensation dynamics", "Standard career progression trajectory"]
            
        return reasons[:3]

explainer = ModelExplainer()
