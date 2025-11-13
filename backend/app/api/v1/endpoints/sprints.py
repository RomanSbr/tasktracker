from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.api.deps import get_db, get_current_user
from app.crud.sprint import sprint as crud_sprint
from app.schemas.sprint import SprintCreate, SprintUpdate, SprintResponse, SprintWithTasks
from app.models.user import User
from app.services.access import ensure_project_access
from app.services.permissions import require_project_permission

router = APIRouter()


@router.get("/projects/{project_id}/sprints", response_model=List[SprintResponse])
async def get_sprints(
    project_id: UUID,
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sprints for project"""
    await ensure_project_access(db, project_id=project_id, user_id=current_user.id)
    sprints = await crud_sprint.get_by_project(
        db,
        project_id=project_id,
        status=status,
        skip=skip,
        limit=limit
    )
    return sprints


@router.get("/projects/{project_id}/sprints/active", response_model=SprintResponse)
async def get_active_sprint(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get active sprint for project"""
    await ensure_project_access(db, project_id=project_id, user_id=current_user.id)
    active_sprint = await crud_sprint.get_active(db, project_id=project_id)
    if not active_sprint:
        raise HTTPException(status_code=404, detail="No active sprint found")
    return active_sprint


@router.post("/projects/{project_id}/sprints", response_model=SprintResponse, status_code=status.HTTP_201_CREATED)
async def create_sprint(
    project_id: UUID,
    sprint_in: SprintCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new sprint"""
    await require_project_permission(
        db,
        project_id=project_id,
        user_id=current_user.id,
        permission_key="MANAGE_SPRINTS"
    )

    if sprint_in.project_id != project_id:
        raise HTTPException(status_code=400, detail="Project ID mismatch")

    sprint = await crud_sprint.create(db, obj_in=sprint_in)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@router.get("/sprints/{sprint_id}", response_model=SprintWithTasks)
async def get_sprint(
    sprint_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sprint by ID with statistics"""
    sprint = await crud_sprint.get(db, id=sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    await ensure_project_access(db, project_id=sprint.project_id, user_id=current_user.id)

    stats = await crud_sprint.get_stats(db, sprint_id=sprint_id)
    return SprintWithTasks(
        **sprint.__dict__,
        **stats
    )


@router.patch("/sprints/{sprint_id}", response_model=SprintResponse)
async def update_sprint(
    sprint_id: UUID,
    sprint_in: SprintUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update sprint"""
    sprint = await crud_sprint.get(db, id=sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    await ensure_project_access(db, project_id=sprint.project_id, user_id=current_user.id)

    sprint = await crud_sprint.update(db, db_obj=sprint, obj_in=sprint_in)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@router.post("/sprints/{sprint_id}/start", response_model=SprintResponse)
async def start_sprint(
    sprint_id: UUID,
    start_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start sprint"""
    sprint = await crud_sprint.get(db, id=sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    await require_project_permission(
        db,
        project_id=sprint.project_id,
        user_id=current_user.id,
        permission_key="MANAGE_SPRINTS"
    )

    if sprint.status == "active":
        raise HTTPException(status_code=400, detail="Sprint is already active")

    # Check if there's another active sprint
    active_sprint = await crud_sprint.get_active(db, project_id=sprint.project_id)
    if active_sprint and active_sprint.id != sprint_id:
        raise HTTPException(
            status_code=400,
            detail=f"Another sprint ({active_sprint.name}) is already active"
        )

    sprint = await crud_sprint.start(db, sprint=sprint, start_date=start_date)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@router.post("/sprints/{sprint_id}/complete", response_model=SprintResponse)
async def complete_sprint(
    sprint_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Complete sprint"""
    sprint = await crud_sprint.get(db, id=sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    await require_project_permission(
        db,
        project_id=sprint.project_id,
        user_id=current_user.id,
        permission_key="MANAGE_SPRINTS"
    )

    if sprint.status == "completed":
        raise HTTPException(status_code=400, detail="Sprint is already completed")

    sprint = await crud_sprint.complete(db, sprint=sprint)
    await db.commit()
    await db.refresh(sprint)
    return sprint


@router.delete("/sprints/{sprint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sprint(
    sprint_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete sprint"""
    sprint = await crud_sprint.get(db, id=sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    await require_project_permission(
        db,
        project_id=sprint.project_id,
        user_id=current_user.id,
        permission_key="MANAGE_SPRINTS"
    )

    if sprint.status == "active":
        raise HTTPException(status_code=400, detail="Cannot delete active sprint")

    await crud_sprint.delete(db, id=sprint_id)
    await db.commit()
    return None

