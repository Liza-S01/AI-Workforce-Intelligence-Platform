import pytest
from pydantic import ValidationError
from app.validation.employee_schema import EmployeePredictRequest

def test_valid_employee_request():
    req = EmployeePredictRequest(
        EmployeeID=101,
        Age=32,
        Department="Research & Development",
        JobRole="Research Scientist",
        MonthlyIncome=5000.0,
        TotalWorkingYears=8,
        YearsAtCompany=3,
        YearsInCurrentRole=2,
        OverTime="Yes"
    )
    assert req.Age == 32
    assert req.MonthlyIncome == 5000.0
    assert req.OverTime == "Yes"

def test_invalid_age_raises_validation_error():
    with pytest.raises(ValidationError):
        EmployeePredictRequest(
            Age=12,  # Must be >= 18
            Department="Sales",
            JobRole="Sales Executive",
            MonthlyIncome=4000.0,
            TotalWorkingYears=2,
            YearsAtCompany=1,
            YearsInCurrentRole=1,
            OverTime="No"
        )

def test_negative_income_raises_validation_error():
    with pytest.raises(ValidationError):
        EmployeePredictRequest(
            Age=30,
            Department="Sales",
            JobRole="Sales Executive",
            MonthlyIncome=-100.0,  # Must be > 0
            TotalWorkingYears=5,
            YearsAtCompany=2,
            YearsInCurrentRole=2,
            OverTime="No"
        )
