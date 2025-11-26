# api/routes_candidates.py
from fastapi import APIRouter
from services.candidate_service import list_candidates

router = APIRouter(prefix="/api", tags=["candidates"])

@router.get("/all-candidates")
def list_candidates_endpoint():
    return list_candidates()