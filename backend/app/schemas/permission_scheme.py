from typing import List, Optional, Dict
from uuid import UUID
from pydantic import BaseModel, Field


class PermissionSchemeRuleBase(BaseModel):
    permission_key: str = Field(..., min_length=1, max_length=100)
    principal_type: str = Field(..., min_length=1, max_length=50)
    principal_identifier: str = Field(..., min_length=1, max_length=255)
    constraints: Optional[Dict[str, str]] = None


class PermissionSchemeRuleCreate(PermissionSchemeRuleBase):
    pass


class PermissionSchemeRuleUpdate(BaseModel):
    constraints: Optional[Dict[str, str]] = None
    principal_type: Optional[str] = None
    principal_identifier: Optional[str] = None


class PermissionSchemeRuleResponse(PermissionSchemeRuleBase):
    id: UUID

    class Config:
        from_attributes = True


class PermissionSchemeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class PermissionSchemeCreate(PermissionSchemeBase):
    organization_id: UUID
    rules: List[PermissionSchemeRuleCreate]


class PermissionSchemeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class PermissionSchemeResponse(PermissionSchemeBase):
    id: UUID
    organization_id: UUID
    rules: List[PermissionSchemeRuleResponse]

    class Config:
        from_attributes = True
