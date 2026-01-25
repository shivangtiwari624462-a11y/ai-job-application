import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "jobs_all.json")
COOKIES_PATH = os.path.join(BASE_DIR, "data", "linkedin_cookies.txt")

SEARCH_URL = (
    "https://www.linkedin.com/jobs/search/"
    "?keywords=frontend%20developer&location=India"
)

# =========================
# HELPERS
# =========================
def load_jobs():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_jobs(jobs):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

def job_exists(jobs, title, company):
    return any(j["title"] == title and j["company"] == company for j in jobs)

# =========================
# MAIN
# =========================
def run():
    print("📂 DATA PATH:", DATA_PATH)
    print("🍪 COOKIES PATH:", COOKIES_PATH)

    if not os.path.exists(COOKIES_PATH):
        raise FileNotFoundError("LinkedIn cookies file missing")

    jobs = load_jobs()
    added = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # -------- COOKIES --------
        cookies = []
        with open(COOKIES_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.strip().split("\t")
                cookies.append({
                    "domain": parts[0],
                    "path": parts[2],
                    "name": parts[5],
                    "value": parts[6],
                })
        context.add_cookies(cookies)

        page = context.new_page()
        page.goto(SEARCH_URL, timeout=60000)
        page.wait_for_timeout(10000)

        # =========================
        # 🔥 HARD SCROLL (KEYBOARD)
        # =========================
        for _ in range(15):
            page.keyboard.press("PageDown")
            page.wait_for_timeout(1200)

        # =========================
        # 🔥 WAIT FOR JOBS TO RENDER
        # =========================
        page.wait_for_timeout(5000)

        # =========================
        # ✅ FINAL STABLE SELECTOR
        # =========================
        cards = page.query_selector_all("li[data-job-id]")
        print(f"🔍 Cards found: {len(cards)}")

        for card in cards[:15]:
            title_el = card.query_selector("h3")
            company_el = card.query_selector("h4")
            link_el = card.query_selector("a")

            if not title_el or not company_el or not link_el:
                continue

            title = title_el.inner_text().strip()
            company = company_el.inner_text().strip()
            link = link_el.get_attribute("href")

            if job_exists(jobs, title, company):
                continue

            jobs.append({
                "title": title,
                "company": company,
                "location": "India",
                "source": "linkedin",
                "link": link,
                "apply_type": "easy_apply",
                "applied": False,
                "date_added": datetime.now().strftime("%Y-%m-%d")
            })
            added += 1

        browser.close()

    save_jobs(jobs)
    print(f"✅ New LinkedIn jobs added: {added}")
    print(f"📦 Total jobs in system: {len(jobs)}")

# =========================
if __name__ == "__main__":
    run()
