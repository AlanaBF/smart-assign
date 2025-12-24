"""Candidate API Routes.

This module defines the FastAPI routes for candidate-related operations.
It handles HTTP requests and delegates business logic to the candidate service.
"""
# api/routes_candidates.py
from fastapi import APIRouter
from services.candidate_service import list_candidates

router = APIRouter(prefix="/api", tags=["candidates"])

@router.get("/all-candidates")
def list_candidates_endpoint():
    """Get all candidates from the database.
    
    Returns:
        list[dict]: A list of candidate dictionaries containing candidate information
            including user_id, full_name, email, department, skills, availability, etc.
        
    Example:
        GET /api/all-candidates
        
        Response::
        
            [
                {
                    "user_id": 123,
                    "full_name": "John Doe",
                    "email": "john.doe@example.com",
                    "department": "Engineering",
                    "skills": "Python, FastAPI, PostgreSQL",
                    "availability": 75,
                    "clearance": "SC"
                }
            ]
    """
    return list_candidates()