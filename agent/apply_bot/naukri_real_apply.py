from playwright.sync_api import sync_playwright
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
COOKIES_FILE = os.path.join(BASE_DIR, "data", "naukri_cookies.txt")
JOBS_FILE = os.path.join(BASE_DIR, "data", "jobs_all.json")

def load_netscape_cookies(context):
    cookies = []
    with open(COOKIES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) != 7:
                continue
            domain, flag, path, secure, expiry, name, value = parts
            cookies.append({
                "domain": domain,
                "path": path,
                "name": name,
                "value": value,
                "secure": secure.upper() == "TRUE",
                "expires": int(expiry)
            })
    context.add_cookies(cookies)

def run_naukri_real_apply():
    if not os.path.exists(COOKIES_FILE):
        print("❌ naukri_cookies.txt not found")
        return

    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        load_netscape_cookies(context)

        page = context.new_page()
        page.goto("https://www.naukri.com", timeout=60000)
        page.wait_for_timeout(5000)

        applied_today = 0

        for job in jobs:
            if job.get("applied"):
                continue

            page.goto(job["apply_link"], timeout=60000)
            page.wait_for_timeout(3000)

            if page.locator("text=Apply").first.is_visible():
                page.locator("text=Apply").first.click()
                job["applied"] = True
                job["status"] = "applied"
                applied_today += 1
                print(f"✅ Applied: {job['title']}")
            else:
                job["status"] = "already_applied"
                print(f"⚠️ Already applied / no button: {job['title']}")

        browser.close()

    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    print(f"🔥 REAL Applications done today: {applied_today}")
