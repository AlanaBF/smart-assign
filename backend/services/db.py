# services/db.py
import os
import configparser
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine

def _read_config() -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parents[1] / "config.ini"
    if not config_path.exists():
        raise FileNotFoundError(f"config.ini not found at {config_path}")
    cfg.read(config_path)
    return cfg

def get_engine() -> Engine:
    cfg = _read_config()
    url = URL.create(
        "postgresql+psycopg2",
        username=cfg.get("postgres", "username"),
        password=cfg.get("postgres", "password"),
        host=cfg.get("postgres", "host"),
        port=cfg.get("postgres", "port"),
        database=cfg.get("postgres", "database"),
    )
    return create_engine(url, pool_pre_ping=True, future=True)

def fetch_all(sql: str, params: dict | None = None):
    """
    Run a SELECT and return a list[dict].
    Used by candidate_service and search_service.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result]
