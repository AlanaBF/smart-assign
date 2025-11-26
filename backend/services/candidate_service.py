# services/candidate_service.py
from services.db import fetch_all

def list_candidates(limit: int = 50, offset: int = 0):
  sql = """
  SELECT *
  FROM cv_search_profile_mv
  LIMIT :limit OFFSET :offset
  """

  rows = fetch_all(sql, {"limit": limit, "offset": offset})

  def pick(row: dict, *candidates):
    for c in candidates:
      if c in row and row[c] is not None:
        return row[c]
    return None

  mapped = []
  for r in rows:
    raw_name = pick(r, "full_name", "user_name", "name")
    raw_skills = pick(r, "skills", "key_qualifications", "technologies")
    skills_str = None
    if raw_skills is None:
      skills_str = None
    elif isinstance(raw_skills, (list, tuple)):
      skills_str = ", ".join([str(s).strip() for s in raw_skills if s])
    else:
      val = str(raw_skills)
      val = val.strip()
      if val.startswith('[') and val.endswith(']'):
        try:
          import json
          arr = json.loads(val)
          if isinstance(arr, list):
            skills_str = ", ".join([str(s).strip() for s in arr if s])
        except Exception:
          skills_str = val.strip('[]').replace("\"", "").replace("'", "")
      else:
        skills_str = val

    raw_av = pick(r, "avg_availability_30d", "availability", "latest_percent_available", "latest_percent_available")
    try:
      availability_val = int(raw_av) if raw_av is not None else 0
    except Exception:
      try:
        availability_val = int(float(raw_av))
      except Exception:
        availability_val = 0

    raw_cpd = pick(r, "cpd_label", "cpd", "cpd_level")
    raw_sfia = pick(r, "sfia_level", "sfia")
    raw_dept = pick(r, "department", "grade", "job_grade", "level")

    grade_display = None
    if raw_cpd and raw_sfia:
      grade_display = f"{raw_cpd} / SFIA{raw_sfia}"
    elif raw_cpd:
      grade_display = str(raw_cpd)
    elif raw_sfia:
      grade_display = f"SFIA{raw_sfia}"
    else:
      grade_display = raw_dept

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

