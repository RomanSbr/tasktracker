from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.crud.task import task as crud_task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatus
from app.schemas.task_history import TaskHistoryResponse
from app.schemas.common import PaginatedResponse
from app.models.user import User
from app.models.task import Task, TaskHistory
from app.services.access import ensure_project_access, ensure_task_access
from app.services.permissions import require_project_permission
from sqlalchemy import select

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
        await ensure_project_access(db, project_id=project_id, user_id=current_user.id)
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

        tasks = await crud_task.get_for_user(
            db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            filters=filters
        )

    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new task"""
    await require_project_permission(
        db,
        project_id=task_in.project_id,
        user_id=current_user.id,
        permission_key="CREATE_ISSUES"
    )
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
    task = await ensure_task_access(db, task_id=task_id, user_id=current_user.id)
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update task"""
    task = await ensure_task_access(db, task_id=task_id, user_id=current_user.id)
    
    # Check permission for status transitions
    if task_in.status and task_in.status != task.status:
        await require_project_permission(
            db,
            project_id=task.project_id,
            user_id=current_user.id,
            permission_key="TRANSITION_ISSUES"
        )
    else:
        await require_project_permission(
            db,
            project_id=task.project_id,
            user_id=current_user.id,
            permission_key="EDIT_ISSUES"
        )

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
    task = await ensure_task_access(db, task_id=task_id, user_id=current_user.id)
    
    await require_project_permission(
        db,
        project_id=task.project_id,
        user_id=current_user.id,
        permission_key="ADMINISTER_PROJECT"
    )

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


@router.post("/projects/{project_id}/backlog/order", status_code=status.HTTP_204_NO_CONTENT)
async def update_backlog_order(
    project_id: UUID,
    task_positions: List[dict],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update backlog task order"""
    await ensure_project_access(db, project_id=project_id, user_id=current_user.id)

    # Validate that all tasks belong to the project
    task_ids = [item.get("task_id") for item in task_positions if item.get("task_id")]
    if task_ids:
        tasks = await db.execute(
            select(Task).where(
                Task.id.in_(task_ids),
                Task.project_id == project_id
            )
        )
        found_tasks = tasks.scalars().all()
        if len(found_tasks) != len(task_ids):
            raise HTTPException(status_code=400, detail="Some tasks not found or don't belong to project")

    await crud_task.update_positions(db, task_positions=task_positions)
    await db.commit()
    return None


@router.get("/projects/{project_id}/backlog", response_model=List[TaskResponse])
async def get_backlog(
    project_id: UUID,
    sprint_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get backlog tasks for project"""
    await ensure_project_access(db, project_id=project_id, user_id=current_user.id)
    tasks = await crud_task.get_backlog_tasks(
        db,
        project_id=project_id,
        sprint_id=sprint_id
    )
    return tasks


@router.get("/{task_id}/history", response_model=List[TaskHistoryResponse])
async def get_task_history(
    task_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task history"""
    await ensure_task_access(db, task_id=task_id, user_id=current_user.id)
    
    query = (
        select(TaskHistory)
        .where(TaskHistory.task_id == task_id)
        .order_by(TaskHistory.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    history = result.scalars().all()
    return history
