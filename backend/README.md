# Backend - Smart-Assign

Minimal instructions to run the FastAPI backend for local development.

Prerequisites

- Python 3.10+
- PostgreSQL accessible from your machine
- A Python virtual environment (recommended)

Setup

1. Create and activate a virtual environment:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the database connection (local only):

- Copy `backend/.env.example` → `backend/.env` and set `PGHOST`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`, and optionally `PGPORT`.
- Do NOT commit `backend/.env` — it is ignored by `.gitignore`.

Run

```bash
# with the venv active
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Quick checks

- Root health: `curl http://127.0.0.1:8000/`
- Candidates: `curl http://127.0.0.1:8000/api/all-candidates | python -m json.tool`

Notes

- The backend expects the ETL to have populated the DB (materialized view `cv_search_profile_mv`).
- DB helpers are in `services/db.py`; candidate logic lives in `services/candidate_service.py`.
