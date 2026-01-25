import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
JOBS_FILE = os.path.join(BASE_DIR, "data", "jobs_all.json")

def run_apply_engine():
    if not os.path.exists(JOBS_FILE):
        print("❌ jobs_all.json not found")
        return

    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    applied_count = 0

    for job in jobs:
        if job.get("applied") is True:
            continue

        if not job.get("apply_type") or not job.get("apply_link"):
            print(f"⚠️ Skipping (missing apply data): {job.get('title')}")
            continue

        print(f"🚀 Applying to: {job['title']} | {job['company']}")
        print(f"➡️ Apply type: {job['apply_type']}")

        job["applied"] = True
        job["status"] = "applied"
        applied_count += 1

    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    print(f"✅ Applications done today: {applied_count}")
