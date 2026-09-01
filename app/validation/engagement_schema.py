from pydantic import BaseModel, Field
from typing import List, Optional

class EngagementRecord(BaseModel):
    EmployeeID: int
    Department: str
    JobRole: str
    EngagementScore: float = Field(..., ge=0, le=100)
    JobSatisfaction: int = Field(..., ge=1, le=4)
    WorkLifeBalance: int = Field(..., ge=1, le=4)

class PolicyQARequest(BaseModel):
    query: str = Field(..., min_length=2, description="Employee question regarding policies")
    policy_category: Optional[str] = Field(default=None, description="Optional specific policy filter")

class PolicyQAResponse(BaseModel):
    query: str
    answer: str
    sources: List[str]
    confidence: float

class ResumeMatchRequest(BaseModel):
    target_role: str = Field(..., description="Job role to match (e.g. ML Engineer, Data Analyst, Backend Engineer)")
    resume_id: Optional[str] = None
    resume_text: Optional[str] = None

class CandidateMatchResult(BaseModel):
    candidate_name: str
    target_role: str
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    recommendation: str
