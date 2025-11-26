# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_candidates import router as candidates_router

app = FastAPI(title="Smart-Assign")

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
    return {"ok": True, "service": "Smart-Assign API (DB)"}
