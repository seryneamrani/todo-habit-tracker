from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class NoteModel(BaseModel):
    title: str = Field(..., min_length=1)
    content: Optional[str] = None
    tags: List[str] = []
    workspace_id: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class NoteUpdateModel(BaseModel):
    title: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]
