from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WorkspaceModel(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    color: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class WorkspaceUpdateModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    color: Optional[str]
