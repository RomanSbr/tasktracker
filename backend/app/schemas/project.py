from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal
import re


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    key: str = Field(..., min_length=2, max_length=10, description="Project key (2-10 uppercase letters)")
    description: Optional[str] = Field(None, max_length=2000)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = Field(None, ge=0)
    workflow_id: Optional[UUID] = None
    permission_scheme_id: Optional[UUID] = None
    lead_id: Optional[UUID] = None

    @field_validator('key')
    @classmethod
    def validate_key(cls, v: str) -> str:
        # Project key should be uppercase letters only, 2-10 chars
        if not re.match(r'^[A-Z]{2,10}$', v.upper()):
            raise ValueError('Project key must contain only uppercase letters (2-10 characters)')
        return v.upper()

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Project name cannot be empty')
        return v.strip()


class ProjectCreate(ProjectBase):
    organization_id: UUID


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None
    workflow_id: Optional[UUID] = None
    permission_scheme_id: Optional[UUID] = None
    lead_id: Optional[UUID] = None


class ProjectResponse(ProjectBase):
    id: UUID
    organization_id: UUID
    status: str
    created_by: UUID
    lead_id: Optional[UUID]
    key_sequence: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProjectWithStats(ProjectResponse):
    total_tasks: int = 0
    completed_tasks: int = 0
    active_tasks: int = 0
    members_count: int = 0
