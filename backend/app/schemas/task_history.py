from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class TaskHistoryResponse(BaseModel):
    id: UUID
    task_id: UUID
    user_id: Optional[UUID]
    action: str
    field_name: Optional[str]
    old_value: Optional[str]
    new_value: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

