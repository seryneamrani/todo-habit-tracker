from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime, timedelta
from database import db
from models.habit_model import HabitModel, HabitUpdateModel

router = APIRouter(prefix="/habits", tags=["Habits"])

# -----------------------------------
# 1️⃣ Ajouter une habitude
# -----------------------------------

@router.post("/")
async def add_habit(habit: HabitModel):
    data = habit.dict()
    result = await db.habits.insert_one(data)
    return {"id": str(result.inserted_id)}

# -----------------------------------
# 2️⃣ Modifier une habitude
# -----------------------------------

@router.put("/{habit_id}")
async def update_habit(habit_id: str, update: HabitUpdateModel):
    try:
        oid = ObjectId(habit_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    changes = {k: v for k, v in update.dict().items() if v is not None}

    await db.habits.update_one({"_id": oid}, {"$set": changes})
    return {"message": "Habit updated successfully"}

# -----------------------------------
# 3️⃣ Marquer une habitude comme faite pour aujourd'hui
# -----------------------------------

@router.post("/{habit_id}/check")
async def check_habit(habit_id: str):
    try:
        oid = ObjectId(habit_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    today = datetime.utcnow().date().isoformat()

    await db.habits.update_one(
        {"_id": oid},
        {"$set": {f"history.{today}": True}}
    )

    return {"message": "Habit checked for today"}

# -----------------------------------
# 4️⃣ Filtrer les habitudes par workspace
# -----------------------------------

@router.get("/")
async def get_habits(workspace_id: str = None):
    query = {}

    if workspace_id:
        query["workspace_id"] = workspace_id

    habits = await db.habits.find(query).to_list(500)
    for h in habits:
        h["_id"] = str(h["_id"])
    return habits

# -----------------------------------
# 5️⃣ Streak automatique
# -----------------------------------

def calculate_streak(history: dict):
    """history is a dict: {"2025-11-20": True, ...}"""

    if not history:
        return {"current_streak": 0, "longest_streak": 0}

    # transform keys into datetime objects
    dates = sorted([datetime.fromisoformat(d).date() for d in history.keys()])

    longest = 1
    current = 1

    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    # check if today continues the streak
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    if str(today) in history:
        pass
    elif str(yesterday) in history:
        current += 1
    else:
        current = 0

    return {
        "current_streak": current,
        "longest_streak": longest
    }

# -----------------------------------
# 6️⃣ Endpoint Stats Habits
# -----------------------------------

@router.get("/stats/{workspace_id}")
async def habit_statistics(workspace_id: str):
    habits = await db.habits.find({"workspace_id": workspace_id}).to_list(500)

    total = len(habits)
    completed_today = 0
    today = datetime.utcnow().date().isoformat()

    for h in habits:
        if h["history"].get(today) is True:
            completed_today += 1

    streaks = {}
    for h in habits:
        streaks[h["name"]] = calculate_streak(h["history"])

    return {
        "total_habits": total,
        "completed_today": completed_today,
        "completion_rate": round((completed_today / total) * 100, 2) if total > 0 else 0,
        "streaks": streaks
    }

# -----------------------------------
# 7️⃣ Heatmap-ready
# -----------------------------------

@router.get("/heatmap/{habit_id}")
async def heatmap(habit_id: str):
    try:
        oid = ObjectId(habit_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    habit = await db.habits.find_one({"_id": oid})

    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    return habit["history"]
