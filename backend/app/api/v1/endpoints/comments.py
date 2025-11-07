from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.crud.comment import comment as crud_comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[CommentResponse])
async def get_comments(
    task_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comments for a task"""
    comments = await crud_comment.get_by_task(
        db, task_id=task_id, skip=skip, limit=limit
    )
    return comments


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new comment"""
    comment_data = comment_in.model_dump()
    comment_data["user_id"] = current_user.id

    from app.models.comment import Comment
    comment = Comment(**comment_data)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.patch("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: UUID,
    comment_in: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update comment"""
    comment = await crud_comment.get(db, id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    comment.content = comment_in.content
    comment.edited = True
    await db.commit()
    await db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete comment"""
    comment = await crud_comment.get(db, id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await crud_comment.delete(db, id=comment_id)
    await db.commit()
    return None
