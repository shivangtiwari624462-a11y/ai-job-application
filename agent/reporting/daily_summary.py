import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
JOBS_FILE = os.path.join(BASE_DIR, "data", "jobs_all.json")

def generate_daily_report():
    if not os.path.exists(JOBS_FILE):
        print("❌ jobs_all.json not found for report")
        return

    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    print("\n📊 DAILY REPORT")
    print("=" * 40)

    for job in jobs:
        status = "applied" if job.get("applied") else "pending"
        print(f"- {job.get('title')} | {job.get('company')} | {status}")

    print("=" * 40)
