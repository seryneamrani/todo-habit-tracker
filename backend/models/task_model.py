from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TaskModel(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    priority: str = Field(..., pattern="^(low|medium|high)$")
    deadline: Optional[str] = None
    tags: List[str] = []
    workspace_id: str
    status: str = Field("to_do", pattern="^(to_do|in_progress|done)$")
    note: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class TaskUpdateModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    deadline: Optional[str]
    tags: Optional[List[str]]
    status: Optional[str] = Field(None, pattern="^(to_do|in_progress|done)$")
    note: Optional[str]
