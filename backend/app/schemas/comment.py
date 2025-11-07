from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)
    parent_comment_id: Optional[UUID] = None


class CommentCreate(CommentBase):
    task_id: UUID


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1)


class CommentResponse(CommentBase):
    id: UUID
    task_id: UUID
    user_id: UUID
    mentioned_users: Optional[List[UUID]]
    edited: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class CommentWithUser(CommentResponse):
    user: Optional[dict] = None
    replies_count: int = 0
