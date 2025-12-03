# services/candidate_service.py
from services.db import fetch_all

def pick(row: dict, *candidates):
    for c in candidates:
        if c in row and row[c] is not None:
            return row[c]
    return None

def format_skills(raw_skills):
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
    try:
        return int(raw_av) if raw_av is not None else 0
    except Exception:
        try:
            return int(float(raw_av))
        except Exception:
            return 0

def format_grade_display(raw_cpd, raw_sfia, raw_dept):
    if raw_cpd and raw_sfia:
        return f"{raw_cpd} / SFIA{raw_sfia}"
    elif raw_cpd:
        return str(raw_cpd)
    elif raw_sfia:
        return f"SFIA{raw_sfia}"
    else:
        return raw_dept

def list_candidates(limit: int = 500, offset: int = 0):
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

