# Backend - Smart-Assign

This folder contains the FastAPI backend for Smart-Assign. It exposes a small set
of HTTP endpoints (currently the candidates endpoints) and connects to a
PostgreSQL database. The instructions below show how to set up a local
development environment, configure the database connection, and run a quick
smoke test.

Prerequisites

- Python 3.10+ (the project uses modern typing features)
- PostgreSQL accessible with a database and user matching `config.ini`
- A virtual environment (recommended)

1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

1. Install dependencies

```bash
pip install -r requirements.txt
```

1. Configure database access

Copy the example config or create a `config.ini` file in the `backend/` folder with a `[postgres]` section. Example:

```ini
[postgres]
username = myuser
password = mypassword
host = localhost
port = 5432
database = flowcase
```

The backend code reads `config.ini` via `services.db._read_config()` so ensure
the file is readable by the running process.

1. Run the app (development)

```bash
source .venv/bin/activate
uvicorn main:app --reload
```

This starts the FastAPI app on `http://127.0.0.1:8000` by default.

1. Smoke tests

Candidates list (used by the frontend Manual Search):

```bash
curl http://127.0.0.1:8000/api/all-candidates | python -m json.tool
```

Root health check:

```bash
curl http://127.0.0.1:8000/
```

Notes and maintenance

- The backend expects a materialized view named `cv_search_profile_mv` in the
  configured database; this is produced by the ETL pipeline in `ETL_pipeline`.
- Core DB helpers are in `services/db.py`; candidate mapping and normalization
  logic is in `services/candidate_service.py`.
- If you remove or rename database fields, update the mapping logic in
  `candidate_service.py` to keep the API shape stable for the frontend.
