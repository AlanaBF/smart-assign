"""Smart-Assign FastAPI Application.

This module contains the main FastAPI application instance and configuration
for the Smart-Assign candidate management system. It sets up CORS middleware
and includes the candidates router for API endpoints.
"""
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_candidates import router as candidates_router

app = FastAPI(
    title="Smart-Assign",
    description="A web application for candidate management and assignment",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates_router)

@app.get("/")
def root():
    """Root endpoint for health check.
    
    Returns:
        dict: A dictionary containing service status and name.
        
    Example:
        >>> response = root()
        >>> print(response)
        {"ok": True, "service": "Smart-Assign API (DB)"}
    """
    return {"ok": True, "service": "Smart-Assign API (DB)"}
