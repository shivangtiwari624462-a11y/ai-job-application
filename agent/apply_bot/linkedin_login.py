from playwright.sync_api import sync_playwright

def linkedin_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.linkedin.com/login")

        print("👉 Browser me LinkedIn login karo")
        print("👉 Login ho jaaye to terminal me ENTER dabao")

        input()

        context.storage_state(path="linkedin_profile.json")
        print("✅ LinkedIn session saved")

        browser.close()

if __name__ == "__main__":
    linkedin_login()
