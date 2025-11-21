from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import db
from models.workspace_model import WorkspaceModel, WorkspaceUpdateModel

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

# 1️⃣ Ajouter un workspace
@router.post("/")
async def create_workspace(workspace: WorkspaceModel):
    data = workspace.dict()
    result = await db.workspaces.insert_one(data)
    return {"id": str(result.inserted_id)}

# 2️⃣ Modifier un workspace
@router.put("/{workspace_id}")
async def update_workspace(workspace_id: str, update: WorkspaceUpdateModel):
    try:
        oid = ObjectId(workspace_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    changes = {k: v for k, v in update.dict().items() if v is not None}
    await db.workspaces.update_one({"_id": oid}, {"$set": changes})
    return {"message": "Workspace updated"}

# 3️⃣ Supprimer un workspace
@router.delete("/{workspace_id}")
async def delete_workspace(workspace_id: str):
    try:
        oid = ObjectId(workspace_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    # Vérifier si lié à tâches/habits
    tasks = await db.tasks.count_documents({"workspace_id": workspace_id})
    habits = await db.habits.count_documents({"workspace_id": workspace_id})

    if tasks > 0 or habits > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete: Workspace contains tasks or habits"
        )

    await db.workspaces.delete_one({"_id": oid})
    return {"message": "Workspace deleted"}

# 4️⃣ Récupérer tous les workspaces
@router.get("/")
async def get_workspaces():
    workspaces = await db.workspaces.find().to_list(500)
    for w in workspaces:
        w["_id"] = str(w["_id"])
    return workspaces

# 5️⃣ Récupérer un workspace par ID
@router.get("/{workspace_id}")
async def get_workspace(workspace_id: str):
    try:
        oid = ObjectId(workspace_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    workspace = await db.workspaces.find_one({"_id": oid})

    if not workspace:
        raise HTTPException(404, "Workspace not found")

    workspace["_id"] = str(workspace["_id"])
    return workspace
