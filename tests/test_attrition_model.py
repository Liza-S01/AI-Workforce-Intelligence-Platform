from app.ml.predictor import predictor
from app.validation.employee_schema import EmployeePredictRequest

def test_attrition_prediction_returns_valid_probability():
    req = EmployeePredictRequest(
        EmployeeID=201,
        Age=45,
        Department="Sales",
        JobRole="Sales Executive",
        MonthlyIncome=9500.0,
        TotalWorkingYears=18,
        YearsAtCompany=10,
        YearsInCurrentRole=6,
        YearsSinceLastPromotion=1,
        OverTime="No",
        JobSatisfaction=4,
        WorkLifeBalance=4,
        DistanceFromHome=3.0
    )
    res = predictor.predict(req)
    
    assert 0.0 <= res.AttritionProbability <= 1.0
    assert res.RiskLevel in ["LOW", "MEDIUM", "HIGH"]
    assert len(res.TopContributingFactors) > 0
    assert res.ModelVersion is not None

def test_high_risk_flagging():
    req_high_risk = EmployeePredictRequest(
        EmployeeID=202,
        Age=22,
        Department="Sales",
        JobRole="Sales Rep",
        MonthlyIncome=2200.0,
        TotalWorkingYears=1,
        YearsAtCompany=1,
        YearsInCurrentRole=0,
        YearsSinceLastPromotion=0,
        OverTime="Yes",
        JobSatisfaction=1,
        WorkLifeBalance=1,
        DistanceFromHome=30.0
    )
    res = predictor.predict(req_high_risk)
    
    assert res.AttritionProbability >= 0.35
    assert res.RiskLevel in ["MEDIUM", "HIGH"]
