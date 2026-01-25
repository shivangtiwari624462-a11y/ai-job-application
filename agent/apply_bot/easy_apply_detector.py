from playwright.sync_api import sync_playwright
from job_queue import get_apply_ready_jobs
import urllib.parse

def auto_apply():
    jobs = get_apply_ready_jobs(limit=2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context(storage_state="linkedin_profile.json")
        page = context.new_page()

        for job in jobs:
            title = job["title"]
            print(f"\n🚀 Applying: {title}")

            query = urllib.parse.quote(title)
            page.goto(f"https://www.linkedin.com/jobs/search/?keywords={query}")
            page.wait_for_timeout(6000)

            job_cards = page.locator("div.job-card-container")
            if job_cards.count() == 0:
                print("❌ No job card")
                continue

            job_cards.first.click()
            page.wait_for_timeout(4000)

            easy_apply = page.locator("button:has-text('Easy Apply')")
            if easy_apply.count() == 0:
                print("❌ Easy Apply not available")
                continue

            easy_apply.first.click()
            page.wait_for_timeout(3000)

            # ✅ Only FIRST STEP submit (safe)
            submit = page.locator("button:has-text('Submit application')")
            if submit.count() > 0:
                submit.first.click()
                print("✅ Application SUBMITTED")
            else:
                print("⚠ Multi-step form — skipped for now")

            page.wait_for_timeout(3000)

        browser.close()

if __name__ == "__main__":
    auto_apply()
