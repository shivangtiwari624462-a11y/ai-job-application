import json
import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
JOBS_FILE = os.path.join(DATA_DIR, "jobs_all.json")

os.makedirs(DATA_DIR, exist_ok=True)

def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_jobs(jobs):
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

def job_exists(jobs, title, company):
    for j in jobs:
        if j["title"] == title and j["company"] == company:
            return True
    return False

def run_naukri_search():
    print("🔍 NAUKRI SEARCH STARTED (AUTO MODE)")
    jobs = load_jobs()
    new_jobs = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(
            "https://www.naukri.com/frontend-developer-jobs",
            timeout=60000
        )

        # AUTO SCROLL (FIXED)
        for _ in range(10):
            page.mouse.wheel(0, 4000)
            time.sleep(2)

        cards = page.query_selector_all("article.jobTuple")
        print(f"📦 Cards found: {len(cards)}")

        for card in cards:
            try:
                title = card.query_selector("a.title").inner_text().strip()
                company = card.query_selector("a.subTitle").inner_text().strip()
                link = card.query_selector("a.title").get_attribute("href")

                if job_exists(jobs, title, company):
                    continue

                jobs.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "source": "naukri",
                    "applied": False,
                    "created_at": datetime.now().isoformat()
                })
                new_jobs += 1

            except:
                continue

        browser.close()

    save_jobs(jobs)
    print(f"✅ New jobs added: {new_jobs}")
    print(f"📊 Total jobs in system: {len(jobs)}")
