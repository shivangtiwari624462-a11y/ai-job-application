from playwright.sync_api import sync_playwright

def naukri_auto_login():
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="naukri-profile",
            headless=False,
            args=["--start-maximized"]
        )

        page = context.new_page()

        # Direct login page
        page.goto("https://www.naukri.com/nlogin/login")

        print("🔐 PLEASE MANUALLY LOGIN NOW")
        print("⏳ Login ke baad profile page open hone do")

        # 2 minute wait – enough for OTP
        page.wait_for_timeout(120000)

        print("💾 Session saved. Ab browser band ho raha hai.")

if __name__ == "__main__":
    naukri_auto_login()
