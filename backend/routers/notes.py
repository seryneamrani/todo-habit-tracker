from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
from database import db
from models.note_model import NoteModel, NoteUpdateModel

router = APIRouter(prefix="/notes", tags=["Notes"])

# 1️⃣ Ajouter une note
@router.post("/")
async def create_note(note: NoteModel):
    data = note.dict()
    result = await db.notes.insert_one(data)
    return {"id": str(result.inserted_id)}

# 2️⃣ Modifier une note
@router.put("/{note_id}")
async def update_note(note_id: str, update: NoteUpdateModel):
    try:
        oid = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    changes = {k: v for k, v in update.dict().items() if v is not None}
    changes["updated_at"] = datetime.utcnow().isoformat()

    await db.notes.update_one({"_id": oid}, {"$set": changes})
    return {"message": "Note updated"}

# 3️⃣ Supprimer une note
@router.delete("/{note_id}")
async def delete_note(note_id: str):
    try:
        oid = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    await db.notes.delete_one({"_id": oid})
    return {"message": "Note deleted"}

# 4️⃣ Récupérer une note par ID
@router.get("/{note_id}")
async def get_note(note_id: str):
    try:
        oid = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")

    note = await db.notes.find_one({"_id": oid})

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note["_id"] = str(note["_id"])
    return note

# 5️⃣ Récupérer les notes d’un workspace
@router.get("/")
async def get_notes(workspace_id: str):
    notes = await db.notes.find({"workspace_id": workspace_id}).to_list(500)
    for n in notes:
        n["_id"] = str(n["_id"])
    return notes

# 6️⃣ Rechercher une note
@router.get("/search/")
async def search_notes(query: str, workspace_id: str):
    results = await db.notes.find({
        "workspace_id": workspace_id,
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"content": {"$regex": query, "$options": "i"}},
            {"tags": {"$regex": query, "$options": "i"}}
        ]
    }).to_list(500)

    for r in results:
        r["_id"] = str(r["_id"])

    return results
