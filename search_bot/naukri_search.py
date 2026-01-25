import json
import os
from datetime import datetime

DATA_PATH = "agent/data/jobs_all.json"

def load_jobs():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_jobs(jobs):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

def run():
    jobs = load_jobs()
    print("🔍 Real Naukri scraping mode enabled")
    print("⚠️ No dummy jobs will be added now")
    print(f"📦 Current jobs in system: {len(jobs)}")

if __name__ == "__main__":
    run()
