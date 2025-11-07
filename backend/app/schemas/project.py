from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    key: str = Field(..., min_length=2, max_length=10)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None


class ProjectCreate(ProjectBase):
    organization_id: UUID


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None


class ProjectResponse(ProjectBase):
    id: UUID
    organization_id: UUID
    status: str
    created_by: UUID
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProjectWithStats(ProjectResponse):
    total_tasks: int = 0
    completed_tasks: int = 0
    active_tasks: int = 0
    members_count: int = 0
