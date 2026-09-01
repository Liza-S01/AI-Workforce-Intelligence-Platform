from fastapi import APIRouter
from typing import List
from app.validation.engagement_schema import ResumeMatchRequest, CandidateMatchResult
from app.services.resume_service import resume_service

router = APIRouter(prefix="/nlp", tags=["AI & NLP Services"])

@router.post("/match-resumes", response_model=List[CandidateMatchResult])
def match_resumes(req: ResumeMatchRequest):
    """
    Screens candidate resumes and ranks similarity against target job description.
    """
    matches = resume_service.match_candidates_to_role(req.target_role)
    results = []
    for m in matches:
        results.append(CandidateMatchResult(
            candidate_name=m["candidate_name"],
            target_role=req.target_role,
            match_score=m["match_score"],
            matched_skills=m["matched_skills"],
            missing_skills=m["missing_skills"],
            recommendation=m["recommendation"]
        ))
    return results

@router.get("/candidates")
def list_candidates():
    """
    Returns list of candidate profiles loaded in system.
    """
    cands = resume_service.get_available_candidates()
    return [{"id": c["id"], "name": c["name"], "filename": c["filename"]} for c in cands]
