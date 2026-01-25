from agent.apply_bot.apply_engine import run_apply_engine
from agent.reporting.daily_summary import generate_daily_report

def main():
    print("🚀 AI JOB APPLICATION SYSTEM STARTED")
    print("MODE: FULLY AUTONOMOUS")

    run_apply_engine()
    generate_daily_report()

if __name__ == "__main__":
    main()
