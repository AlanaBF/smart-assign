"""Database Connection and Query Module.

This module handles database connections and queries for the Smart-Assign application.
It uses SQLAlchemy with PostgreSQL and supports environment-based configuration.
"""
# services/db.py
import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine

from dotenv import load_dotenv


def _load_dotenv() -> None:
    """Load backend/.env if present. Intentionally simple: fail silently if missing.
    
    Looks for a .env file in the parent directory of this module and loads
    environment variables from it using python-dotenv.
    """
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)


def _build_url_from_env() -> URL:
    """Build a SQLAlchemy URL from environment variables.

    Required env vars: PGHOST, PGUSER, PGPASSWORD, PGDATABASE
    Optional: PGPORT (defaults to 5432)
    
    Returns:
        URL: SQLAlchemy URL object for PostgreSQL connection.
        
    Raises:
        RuntimeError: If any required environment variables are missing.
        
    Example:
        Environment variables:
        PGHOST=localhost
        PGUSER=myuser
        PGPASSWORD=mypass
        PGDATABASE=smartassign
        PGPORT=5432
        
        Returns URL equivalent to:
        postgresql+psycopg2://myuser:mypass@localhost:5432/smartassign
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
    """Create and return a SQLAlchemy engine instance.
    
    Loads environment variables and creates a PostgreSQL engine with
    connection pooling and pre-ping enabled.
    
    Returns:
        Engine: Configured SQLAlchemy engine instance.
        
    Raises:
        RuntimeError: If required database environment variables are missing.
        
    Example:
        >>> engine = get_engine()
        >>> with engine.connect() as conn:
        ...     result = conn.execute(text("SELECT 1"))
    """
    _load_dotenv()
    url = _build_url_from_env()
    return create_engine(url, pool_pre_ping=True, future=True)


def fetch_all(sql: str, params: dict | None = None):
    """Execute a SELECT query and return all results as a list of dictionaries.
    
    Args:
        sql (str): SQL query string. Use named parameters with :param_name syntax.
        params (dict | None, optional): Dictionary of query parameters. Defaults to None.
        
    Returns:
        list[dict]: List of dictionaries where each dict represents a row.
        Keys are column names and values are the corresponding row values.
        
    Raises:
        Exception: Database connection or query execution errors.
        
    Example:
        >>> sql = "SELECT * FROM users WHERE department = :dept LIMIT :limit"
        >>> params = {"dept": "Engineering", "limit": 10}
        >>> results = fetch_all(sql, params)
        >>> print(len(results))
        10
        >>> print(results[0]['email'])
        'john.doe@example.com'
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result]
