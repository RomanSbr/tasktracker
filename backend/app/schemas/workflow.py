from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class WorkflowStatusBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    order: int = 0
    category: str = Field(default="todo", pattern="^(todo|in_progress|done)$")


class WorkflowStatusCreate(WorkflowStatusBase):
    pass


class WorkflowStatusUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    order: Optional[int] = None
    category: Optional[str] = Field(default=None, pattern="^(todo|in_progress|done)$")


class WorkflowStatusResponse(WorkflowStatusBase):
    id: UUID

    class Config:
        from_attributes = True


class WorkflowBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(default="software")
    is_default: bool = False


class WorkflowCreate(WorkflowBase):
    organization_id: UUID
    statuses: List[WorkflowStatusCreate]


class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_default: Optional[bool] = None


class WorkflowResponse(WorkflowBase):
    id: UUID
    organization_id: UUID
    statuses: List[WorkflowStatusResponse]

    class Config:
        from_attributes = True
