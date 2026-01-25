import json
import os

APPROVAL_QUEUE = "agent/data/approval_queue.json"


def _load_queue():
    if not os.path.exists(APPROVAL_QUEUE):
        return []
    with open(APPROVAL_QUEUE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_queue(data):
    with open(APPROVAL_QUEUE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# 🔹 CALLED WHEN SCORE = 50–69
def request_approval(job):
    queue = _load_queue()

    entry = {
        "job_id": job.get("id"),
        "title": job.get("title"),
        "company": job.get("company"),
        "status": "PENDING"
    }

    queue.append(entry)
    _save_queue(queue)

    print(f"📩 Approval required: {job.get('title')}")
    return "PENDING"


# 🔹 CALLED ON NEXT RUN
def check_approval(job):
    queue = _load_queue()

    for item in queue:
        if item["job_id"] == job.get("id"):
            return item.get("status", "PENDING")

    return "PENDING"
