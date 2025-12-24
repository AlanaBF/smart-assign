"""Candidate Service Module.

This module provides business logic for candidate management operations.
It handles data retrieval, formatting, and transformation of candidate information
from the database layer.
"""
# services/candidate_service.py
from services.db import fetch_all

def pick(row: dict, *candidates):
    """Extract the first non-None value from a dictionary using candidate keys.
    
    Args:
        row (dict): The dictionary to search in.
        *candidates: Variable number of candidate keys to try in order.
        
    Returns:
        Any: The first non-None value found, or None if all candidates are None or missing.
        
    Example:
        >>> data = {"name": None, "full_name": "John Doe", "username": "jdoe"}
        >>> pick(data, "name", "full_name", "username")
        "John Doe"
    """
    for c in candidates:
        if c in row and row[c] is not None:
            return row[c]
    return None

def format_skills(raw_skills):
    """Format skills data into a comma-separated string.
    
    Handles various input formats including lists, tuples, JSON strings,
    and bracket-wrapped strings.
    
    Args:
        raw_skills: Skills data in various formats (list, tuple, string, JSON string, etc.).
        
    Returns:
        str or None: Comma-separated string of skills, or None if input is None.
        
    Example:
        >>> format_skills(["Python", "FastAPI", "PostgreSQL"])
        "Python, FastAPI, PostgreSQL"
        >>> format_skills('["React", "TypeScript"]')
        "React, TypeScript"
    """
    if raw_skills is None:
        return None
    if isinstance(raw_skills, (list, tuple)):
        return ", ".join([str(s).strip() for s in raw_skills if s])
    val = str(raw_skills).strip()
    if val.startswith('[') and val.endswith(']'):
        try:
            import json
            arr = json.loads(val)
            if isinstance(arr, list):
                return ", ".join([str(s).strip() for s in arr if s])
        except Exception:
            return val.strip('[]').replace("\"", "").replace("'", "")
    return val

def parse_availability(raw_av):
    """Parse availability data into an integer percentage.
    
    Args:
        raw_av: Raw availability data (int, float, string, or None).
        
    Returns:
        int: Availability as an integer percentage (0-100), defaults to 0 if parsing fails.
        
    Example:
        >>> parse_availability("75.5")
        75
        >>> parse_availability(None)
        0
    """
    try:
        return int(raw_av) if raw_av is not None else 0
    except Exception:
        try:
            return int(float(raw_av))
        except Exception:
            return 0

def format_grade_display(raw_cpd, raw_sfia, raw_dept):
    """Format grade information for display.
    
    Combines CPD level, SFIA level, and department information into a readable string.
    
    Args:
        raw_cpd: CPD (Continuing Professional Development) level.
        raw_sfia: SFIA (Skills Framework for the Information Age) level.
        raw_dept: Department or fallback grade information.
        
    Returns:
        str: Formatted grade display string.
        
    Example:
        >>> format_grade_display("Senior", "5", "Engineering")
        "Senior / SFIA5"
        >>> format_grade_display(None, "4", "Marketing")
        "SFIA4"
        >>> format_grade_display(None, None, "Sales")
        "Sales"
    """
    if raw_cpd and raw_sfia:
        return f"{raw_cpd} / SFIA{raw_sfia}"
    elif raw_cpd:
        return str(raw_cpd)
    elif raw_sfia:
        return f"SFIA{raw_sfia}"
    else:
        return raw_dept

def list_candidates(limit: int = 500, offset: int = 0):
    """Retrieve and format a list of candidates from the database.
    
    Fetches candidate data from the cv_search_profile_mv materialized view
    and formats it for API consumption.
    
    Args:
        limit (int, optional): Maximum number of candidates to return. Defaults to 500.
        offset (int, optional): Number of candidates to skip for pagination. Defaults to 0.
        
    Returns:
        list[dict]: A list of dictionaries containing formatted candidate information.
        Each dictionary includes:
        - user_id: Unique identifier for the candidate
        - full_name: Candidate's full name
        - user_name: Candidate's username (same as full_name)
        - email: Candidate's email address
        - department: Formatted grade/department information
        - country: Location information
        - latest_cv_title: Most recent CV title/role
        - skills: Comma-separated list of skills
        - availability: Availability percentage (0-100)
        - clearance: Security clearance level
        
    Raises:
        Exception: May raise database connection or query execution errors.
        
    Example:
        >>> candidates = list_candidates(limit=10, offset=0)
        >>> len(candidates)
        10
        >>> candidates[0]['skills']
        "Python, FastAPI, PostgreSQL"
    """
    sql = """
    SELECT *
    FROM cv_search_profile_mv
    LIMIT :limit OFFSET :offset
    """
    rows = fetch_all(sql, {"limit": limit, "offset": offset})

    mapped = []
    for r in rows:
        raw_name = pick(r, "full_name", "user_name", "name")
        raw_skills = pick(r, "skills", "key_qualifications", "technologies")
        skills_str = format_skills(raw_skills)
        raw_av = pick(r, "avg_availability_30d", "availability", "latest_percent_available", "latest_percent_available")
        availability_val = parse_availability(raw_av)
        raw_cpd = pick(r, "cpd_label", "cpd", "cpd_level")
        raw_sfia = pick(r, "sfia_level", "sfia")
        raw_dept = pick(r, "department", "grade", "job_grade", "level")
        grade_display = format_grade_display(raw_cpd, raw_sfia, raw_dept)

        mapped.append({
            "user_id": r.get("user_id"),
            "full_name": raw_name,
            "user_name": raw_name,
            "email": pick(r, "email", "user_email"),
            "department": grade_display,
            "country": pick(r, "country", "location", "city", "region"),
            "latest_cv_title": pick(r, "latest_cv_title", "cv_title"),
            "skills": skills_str,
            "availability": availability_val,
            "clearance": pick(r, "clearance", "sc_clearance", "security_clearance"),
        })

    return mapped

