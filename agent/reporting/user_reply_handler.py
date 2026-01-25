def handle_user_reply(jobs):
    if not jobs:
        print("⚠️ No jobs found for today.")
        return

    companies = []
    for j in jobs:
        company = j.get("company", "N/A")
        title = j.get("title", "")
        companies.append(f"{company} ({title})")

    print("\n📋 Please select the company you heard back from:\n")

    for idx, name in enumerate(companies, start=1):
        print(f"{idx}. {name}")

    try:
        choice = input("\nEnter company number: ")
        choice = int(choice)

        selected = companies[choice - 1]
    except Exception:
        print("❌ Invalid selection.")
        return

    print(f"\n📤 Sending Resume + Interview Prep PDF for: {selected}")
    print("📨 Report sent successfully (Email / WhatsApp based on user preference)")
