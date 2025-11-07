from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum


class TaskStatus(str, Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    TESTING = "testing"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(str, Enum):
    TASK = "task"
    BUG = "bug"
    FEATURE = "feature"
    IMPROVEMENT = "improvement"
    EPIC = "epic"
    STORY = "story"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.BACKLOG
    priority: TaskPriority = TaskPriority.MEDIUM
    type: TaskType = TaskType.TASK
    assignee_id: Optional[UUID] = None
    parent_task_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    story_points: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = []


class TaskCreate(TaskBase):
    project_id: UUID


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    type: Optional[TaskType] = None
    assignee_id: Optional[UUID] = None
    sprint_id: Optional[UUID] = None
    due_date: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    story_points: Optional[int] = Field(None, ge=0)
    tags: Optional[List[str]] = None
    logged_hours: Optional[float] = Field(None, ge=0)


class TaskResponse(TaskBase):
    id: UUID
    project_id: UUID
    task_number: int
    reporter_id: UUID
    logged_hours: float
    position: int
    created_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


class TaskWithDetails(TaskResponse):
    assignee: Optional[dict] = None
    reporter: Optional[dict] = None
    comments_count: int = 0
    attachments_count: int = 0
    watchers_count: int = 0
