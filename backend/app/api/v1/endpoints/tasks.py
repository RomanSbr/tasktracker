from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.crud.task import task as crud_task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatus
from app.schemas.common import PaginatedResponse
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[UUID] = None,
    status: Optional[TaskStatus] = None,
    assignee_id: Optional[UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get tasks with filters"""
    if project_id:
        tasks = await crud_task.get_by_project(
            db,
            project_id=project_id,
            skip=skip,
            limit=limit,
            status=status.value if status else None
        )
    else:
        filters = {}
        if status:
            filters["status"] = status.value
        if assignee_id:
            filters["assignee_id"] = assignee_id

        tasks = await crud_task.get_multi(db, skip=skip, limit=limit, filters=filters)

    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new task"""
    task = await crud_task.create_with_number(
        db,
        obj_in=task_in,
        reporter_id=current_user.id
    )

    # Add history record
    await crud_task.add_history(
        db,
        task_id=task.id,
        user_id=current_user.id,
        action="created"
    )

    await db.commit()
    await db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task by ID"""
    task = await crud_task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update task"""
    task = await crud_task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Record changes in history
    update_data = task_in.model_dump(exclude_unset=True)
    for field, new_value in update_data.items():
        old_value = getattr(task, field, None)
        if old_value != new_value:
            await crud_task.add_history(
                db,
                task_id=task.id,
                user_id=current_user.id,
                action="updated",
                field_name=field,
                old_value=str(old_value) if old_value else None,
                new_value=str(new_value) if new_value else None
            )

    task = await crud_task.update(db, db_obj=task, obj_in=task_in)
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete task"""
    task = await crud_task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Add history before deletion
    await crud_task.add_history(
        db,
        task_id=task.id,
        user_id=current_user.id,
        action="deleted"
    )

    await crud_task.delete(db, id=task_id)
    await db.commit()
    return None
