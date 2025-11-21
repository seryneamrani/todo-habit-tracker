from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class HabitModel(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    workspace_id: str
    history: Dict[str, bool] = {}  # ex: {"2025-11-22": True}
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class HabitUpdateModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
