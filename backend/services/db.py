# services/db.py
import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine

from dotenv import load_dotenv


def _load_dotenv() -> None:
    """Load backend/.env if present. Intentionally simple: fail silently if missing."""
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)


def _build_url_from_env() -> URL:
    """Build a SQLAlchemy URL from environment variables.

    Required env vars: PGHOST, PGUSER, PGPASSWORD, PGDATABASE
    Optional: PGPORT (defaults to 5432)
    """
    host = os.getenv("PGHOST")
    user = os.getenv("PGUSER")
    pwd = os.getenv("PGPASSWORD")
    dbname = os.getenv("PGDATABASE")
    port = os.getenv("PGPORT") or "5432"
    if not (host and user and pwd and dbname):
        raise RuntimeError(
            "Database connection requires PGHOST, PGUSER, PGPASSWORD and PGDATABASE environment variables"
        )
    return URL.create(
        "postgresql+psycopg2",
        username=user,
        password=pwd,
        host=host,
        port=port,
        database=dbname,
    )


def get_engine() -> Engine:
    _load_dotenv()
    url = _build_url_from_env()
    return create_engine(url, pool_pre_ping=True, future=True)


def fetch_all(sql: str, params: dict | None = None):
    """Run a SELECT and return a list[dict]."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result]
