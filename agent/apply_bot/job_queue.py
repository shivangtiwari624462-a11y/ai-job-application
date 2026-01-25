import json
from pathlib import Path

DATA_PATH = Path("agent/apply_bot/data/jobs_all.json")


def load_jobs():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_jobs(jobs):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)


def get_today_jobs():
    jobs = load_jobs()
    easy = [j for j in jobs if not j.get("applied")]
    return [], easy


def mark_applied(job, applied=True, apply_type="form_fill"):
    jobs = load_jobs()
    for j in jobs:
        if j.get("title") == job.get("title"):
            j["applied"] = applied
            j["apply_type"] = apply_type
    save_jobs(jobs)
