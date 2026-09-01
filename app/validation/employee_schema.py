from pydantic import BaseModel, Field
from typing import Optional, List

class EmployeePredictRequest(BaseModel):
    EmployeeID: Optional[int] = Field(default=101, description="Employee unique identifier")
    Age: int = Field(..., ge=18, le=100, description="Age between 18 and 100")
    DailyRate: Optional[float] = Field(default=800.0)
    DistanceFromHome: float = Field(default=5.0, ge=0)
    HourlyRate: Optional[float] = Field(default=65.0)
    MonthlyIncome: float = Field(..., gt=0, description="Monthly salary")
    MonthlyRate: Optional[float] = Field(default=15000.0)
    NumCompaniesWorked: int = Field(default=2, ge=0)
    PercentSalaryHike: float = Field(default=12.0, ge=0)
    TotalWorkingYears: int = Field(..., ge=0)
    TrainingTimesLastYear: int = Field(default=2, ge=0)
    YearsAtCompany: int = Field(..., ge=0)
    YearsInCurrentRole: int = Field(..., ge=0)
    YearsSinceLastPromotion: int = Field(default=0, ge=0)
    YearsWithCurrManager: int = Field(default=2, ge=0)
    EnvironmentSatisfaction: int = Field(default=3, ge=1, le=4)
    JobInvolvement: int = Field(default=3, ge=1, le=4)
    JobLevel: int = Field(default=2, ge=1, le=5)
    JobSatisfaction: int = Field(default=3, ge=1, le=4)
    RelationshipSatisfaction: int = Field(default=3, ge=1, le=4)
    WorkLifeBalance: int = Field(default=3, ge=1, le=4)
    
    # Categoricals
    BusinessTravel: str = Field(default="Travel_Rarely")
    Department: str = Field(..., description="e.g. Sales, Research & Development, Human Resources")
    EducationField: Optional[str] = Field(default="Life Sciences")
    Gender: Optional[str] = Field(default="Female")
    JobRole: str = Field(..., description="Role title")
    MaritalStatus: Optional[str] = Field(default="Single")
    OverTime: str = Field(..., description="Yes or No")

class EmployeePredictResponse(BaseModel):
    EmployeeID: Optional[int]
    AttritionProbability: float
    RiskLevel: str  # HIGH, MEDIUM, LOW
    TopContributingFactors: List[str]
    ModelVersion: str
    Timestamp: str

class EmployeeRecordSchema(BaseModel):
    EmployeeID: int
    Department: str
    JobRole: str
    AttritionProbability: float
    RiskLevel: str
    EngagementScore: float
    CurrentSkills: List[str]
    MissingSkills: List[str]
    RecommendedCourses: List[str]
