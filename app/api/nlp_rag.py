from fastapi import APIRouter
from app.validation.engagement_schema import PolicyQARequest, PolicyQAResponse
from app.services.rag_service import rag_service

router = APIRouter(prefix="/nlp", tags=["AI & NLP Services"])

@router.post("/policy-qa", response_model=PolicyQAResponse)
def query_hr_policies(req: PolicyQARequest):
    """
    RAG-powered policy QA engine for querying HR handbook, leave, remote work, and compensation policies.
    """
    result = rag_service.query(req.query)
    return PolicyQAResponse(
        query=result["query"],
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )
