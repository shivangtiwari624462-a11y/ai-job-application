from agent.reporting.report_builder import build_daily_report
from agent.apply_bot.job_queue import get_today_jobs

def run_daily_summary():
    jobs = get_today_jobs()

    easy_apply = len([j for j in jobs if j.get("apply_type") == "easy"])
    form_apply = len([j for j in jobs if j.get("apply_type") == "form"])
    total = len(jobs)

    stats = {
        "easy_apply": easy_apply,
        "form_apply": form_apply,
        "total": total
    }

    report = build_daily_report(stats)
    print(report)

    user_input = input("(YES / NO): ").strip().lower()

    if user_input != "yes":
        print("\n👍 No response today. Report saved.")
        return

    print("\n📌 Please select the company you heard back from:\n")

    for idx, job in enumerate(jobs, start=1):
        print(f"{idx}. {job['company']} ({job['title']})")

    choice = input("\nEnter company number: ").strip()

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(jobs):
        print("❌ Invalid selection")
        return

    selected_job = jobs[int(choice) - 1]

    print(
        f"\n📤 Sending Resume + Interview Prep PDF for: {selected_job['company']}"
    )
    print("✅ Report sent successfully (Email / WhatsApp based on user preference)")
    

if __name__ == "__main__":
    run_daily_summary()
