from fastapi import APIRouter
from database import db
from datetime import datetime, timedelta
from bson import ObjectId
from routers.habits import calculate_streak

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# -----------------------------------------
# 1️⃣ TASKS ANALYTICS
# -----------------------------------------

async def tasks_analytics():
    tasks = await db.tasks.find().to_list(2000)

    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("status") == "done")
    overdue = sum(1 for t in tasks if t.get("deadline") and t["deadline"] < datetime.utcnow().date().isoformat())

    # priority distribution
    priorities = {"low": 0, "medium": 0, "high": 0}
    for t in tasks:
        if t.get("priority") in priorities:
            priorities[t["priority"]] += 1

    # tasks created per day (last 7 days)
    daily_counts = {}
    for t in tasks:
        d = t.get("created_at", "")[:10]
        daily_counts[d] = daily_counts.get(d, 0) + 1

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "completion_rate": round((completed / total) * 100, 2) if total > 0 else 0,
        "overdue_tasks": overdue,
        "priority_distribution": priorities,
        "tasks_per_day": daily_counts
    }

# -----------------------------------------
# 2️⃣ HABITS ANALYTICS
# -----------------------------------------

async def habits_analytics():
    habits = await db.habits.find().to_list(2000)

    total = len(habits)
    today = datetime.utcnow().date().isoformat()
    completed_today = 0
    streaks = {}

    for h in habits:
        # completed today
        if h.get("history", {}).get(today) is True:
            completed_today += 1

        # streaks
        streaks[h["name"]] = calculate_streak(h.get("history", {}))

    longest_streak = max((s["longest_streak"] for s in streaks.values()), default=0)

    return {
        "total_habits": total,
        "completed_today": completed_today,
        "completion_rate_today": round((completed_today / total) * 100, 2) if total > 0 else 0,
        "streaks": streaks,
        "longest_global_streak": longest_streak
    }

# -----------------------------------------
# 3️⃣ NOTES ANALYTICS
# -----------------------------------------

async def notes_analytics():
    notes = await db.notes.find().to_list(2000)

    total = len(notes)

    # tags distribution
    tag_count = {}
    for n in notes:
        for tag in n.get("tags", []):
            tag_count[tag] = tag_count.get(tag, 0) + 1

    # daily creation
    daily_counts = {}
    for n in notes:
        d = n.get("created_at", "")[:10]
        daily_counts[d] = daily_counts.get(d, 0) + 1

    # avg word count
    word_counts = []
    for n in notes:
        if n.get("content"):
            word_counts.append(len(n["content"].split()))

    avg_words = round(sum(word_counts) / len(word_counts), 2) if word_counts else 0

    return {
        "total_notes": total,
        "avg_words_per_note": avg_words,
        "notes_per_day": daily_counts,
        "tags_distribution": tag_count
    }

# -----------------------------------------
# 4️⃣ WORKSPACES ANALYTICS
# -----------------------------------------

async def workspace_analytics():
    workspaces = await db.workspaces.find().to_list(500)
    tasks = await db.tasks.find().to_list(2000)
    habits = await db.habits.find().to_list(2000)
    notes = await db.notes.find().to_list(2000)

    data = []

    for w in workspaces:
        wid = str(w["_id"])
        data.append({
            "workspace_id": wid,
            "name": w["name"],
            "tasks": sum(1 for t in tasks if t["workspace_id"] == wid),
            "habits": sum(1 for h in habits if h["workspace_id"] == wid),
            "notes": sum(1 for n in notes if n["workspace_id"] == wid),
        })

    return {
        "total_workspaces": len(workspaces),
        "workspaces": data
    }


# -----------------------------------------
# 5️⃣ ENDPOINT GLOBAL ANALYTICS
# -----------------------------------------

@router.get("/")
async def global_analytics():
    return {
        "tasks": await tasks_analytics(),
        "habits": await habits_analytics(),
        "notes": await notes_analytics(),
        "workspaces": await workspace_analytics()
    }
