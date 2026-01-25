import time
from datetime import datetime
from agent.reporting.preferences_loader import load_user_preferences
from agent.reporting.daily_summary import generate_daily_summary


def run_scheduler():
    prefs = load_user_preferences()
    report_time = prefs.get("daily_report_time", "21:00")

    print("⏰ Daily Scheduler started")
    print(f"📅 Report scheduled at {report_time}")

    while True:
        now = datetime.now().strftime("%H:%M")

        if now == report_time:
            print("🚀 Running Daily Job Report...")
            generate_daily_summary()
            print("✅ Report completed. Sleeping for 24 hours.")
            time.sleep(60 * 60 * 24)

        time.sleep(30)


if __name__ == "__main__":
    run_scheduler()
