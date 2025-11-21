from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
from models.task_model import TaskModel, TaskUpdateModel
from database import db

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# ----- 1. Ajouter une tâche -----
@router.post("/")
async def add_task(task: TaskModel):
    task_dict = task.dict()
    result = await db.tasks.insert_one(task_dict)
    return {"id": str(result.inserted_id)}

# ----- 2. Modifier une tâche -----
@router.put("/{task_id}")
async def update_task(task_id: str, update: TaskUpdateModel):
    try:
        oid = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    updated = {k: v for k, v in update.dict().items() if v is not None}
    await db.tasks.update_one({"_id": oid}, {"$set": updated})

    return {"message": "Task updated successfully"}

# ----- 3. Supprimer une tâche -----
@router.delete("/{task_id}")
async def delete_task(task_id: str):
    try:
        oid = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    await db.tasks.delete_one({"_id": oid})

    return {"message": "Task deleted successfully"}

# ----- 4. Filtrer les tâches -----
@router.get("/")
async def filter_tasks(
    status: str = None,
    priority: str = None,
    tag: str = None,
    workspace_id: str = None,
    deadline_before: str = None,
    deadline_after: str = None
):
    query = {}

    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    if tag:
        query["tags"] = tag
    if workspace_id:
        query["workspace_id"] = workspace_id
    if deadline_before:
        query["deadline"] = {"$lte": deadline_before}
    if deadline_after:
        query["deadline"] = {"$gte": deadline_after}

    tasks = await db.tasks.find(query).to_list(500)
    for t in tasks:
        t["_id"] = str(t["_id"])

    return tasks

# ----- 5. Kanban view -----
@router.get("/kanban/{workspace_id}")
async def kanban_view(workspace_id: str):
    statuses = ["to_do", "in_progress", "done"]
    kanban = {}

    for s in statuses:
        results = await db.tasks.find({"workspace_id": workspace_id, "status": s}).to_list(200)
        for r in results:
            r["_id"] = str(r["_id"])
        kanban[s] = results
    
    return kanban

# ----- 6. Vue liste -----
@router.get("/list/{workspace_id}")
async def list_view(workspace_id: str, sort_by: str = "created_at"):
    tasks = await db.tasks.find({"workspace_id": workspace_id}).sort(sort_by, 1).to_list(500)
    for t in tasks:
        t["_id"] = str(t["_id"])
    return tasks

# ----- 7. Overdue -----
@router.get("/overdue/{workspace_id}")
async def overdue_tasks(workspace_id: str):
    today = datetime.utcnow().date().isoformat()

    tasks = await db.tasks.find({
        "workspace_id": workspace_id,
        "deadline": {"$lt": today},
        "status": {"$ne": "done"}
    }).to_list(200)

    for t in tasks:
        t["_id"] = str(t["_id"])

    return tasks

# ----- 8. Stats -----
@router.get("/stats/{workspace_id}")
async def task_statistics(workspace_id: str):
    total = await db.tasks.count_documents({"workspace_id": workspace_id})
    completed = await db.tasks.count_documents({"workspace_id": workspace_id, "status": "done"})
    in_progress = await db.tasks.count_documents({"workspace_id": workspace_id, "status": "in_progress"})
    todo = await db.tasks.count_documents({"workspace_id": workspace_id, "status": "to_do"})

    low = await db.tasks.count_documents({"workspace_id": workspace_id, "priority": "low"})
    medium = await db.tasks.count_documents({"workspace_id": workspace_id, "priority": "medium"})
    high = await db.tasks.count_documents({"workspace_id": workspace_id, "priority": "high"})

    return {
        "total_tasks": total,
        "completed": completed,
        "in_progress": in_progress,
        "todo": todo,
        "completion_rate": (completed / total * 100) if total > 0 else 0,
        "priorities": {
            "low": low,
            "medium": medium,
            "high": high
        }
    }
