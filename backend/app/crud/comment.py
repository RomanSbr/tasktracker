from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    async def get_by_task(
        self, db: AsyncSession, *, task_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        """Get comments by task"""
        query = (
            select(Comment)
            .where(Comment.task_id == task_id, Comment.parent_comment_id.is_(None))
            .offset(skip)
            .limit(limit)
            .order_by(Comment.created_at.asc())
        )
        result = await db.execute(query)
        return result.scalars().all()


comment = CRUDComment(Comment)
