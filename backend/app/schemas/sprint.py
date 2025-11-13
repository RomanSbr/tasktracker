from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class SprintBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    goal: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SprintCreate(SprintBase):
    project_id: UUID


class SprintUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    goal: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SprintResponse(SprintBase):
    id: UUID
    project_id: UUID
    status: str
    sprint_number: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class SprintWithTasks(SprintResponse):
    tasks_count: int = 0
    completed_tasks_count: int = 0
    total_story_points: Optional[int] = 0
    completed_story_points: Optional[int] = 0

