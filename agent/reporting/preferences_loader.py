import json
import os

PREF_FILE = "agent/reporting/user_preferences.json"


def load_user_preferences():
    if not os.path.exists(PREF_FILE):
        return {
            "delivery_mode": "email",
            "daily_report_time": "21:00",
            "send_interview_material": True
        }

    with open(PREF_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
