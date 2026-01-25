# agent/reporting/preferences.py

import json
import os

PREF_FILE = "agent/reporting/user_preferences.json"


DEFAULT_PREFS = {
    "delivery_mode": "email",   # email | whatsapp | both
    "daily_report_time": "21:00",  # 24-hr format HH:MM
    "send_interview_material": True
}


def load_preferences():
    if not os.path.exists(PREF_FILE):
        save_preferences(DEFAULT_PREFS)
        return DEFAULT_PREFS

    with open(PREF_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_preferences(prefs):
    os.makedirs(os.path.dirname(PREF_FILE), exist_ok=True)
    with open(PREF_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=4)


def setup_preferences():
    print("\n⚙️ USER PREFERENCES SETUP\n")

    print("How should reports be sent?")
    print("1. Email")
    print("2. WhatsApp")
    print("3. Both")

    choice = input("Choose option (1/2/3): ").strip()

    if choice == "1":
        delivery = "email"
    elif choice == "2":
        delivery = "whatsapp"
    else:
        delivery = "both"

    report_time = input("Daily report time (HH:MM, 24hr format) [default 21:00]: ").strip()
    if not report_time:
        report_time = "21:00"

    prefs = {
        "delivery_mode": delivery,
        "daily_report_time": report_time,
        "send_interview_material": True
    }

    save_preferences(prefs)

    print("\n✅ Preferences saved successfully:")
    print(prefs)


if __name__ == "__main__":
    setup_preferences()
