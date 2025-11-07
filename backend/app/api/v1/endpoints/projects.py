from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.crud.project import project as crud_project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    organization_id: Optional[UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get projects"""
    if organization_id:
        projects = await crud_project.get_by_organization(
            db, organization_id=organization_id, skip=skip, limit=limit
        )
    else:
        projects = await crud_project.get_multi(db, skip=skip, limit=limit)
    return projects


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new project"""
    # Check if project key already exists
    existing = await crud_project.get_by_key(db, key=project_in.key.upper())
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Project with this key already exists"
        )

    # Create project
    project_data = project_in.model_dump()
    project_data["key"] = project_in.key.upper()
    project_data["created_by"] = current_user.id

    from app.schemas.project import ProjectCreate as PC
    project = await crud_project.create(
        db,
        obj_in=PC(**project_data)
    )

    await db.commit()
    await db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get project by ID"""
    project = await crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_in: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update project"""
    project = await crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project = await crud_project.update(db, db_obj=project, obj_in=project_in)
    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete project"""
    project = await crud_project.get(db, id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await crud_project.delete(db, id=project_id)
    await db.commit()
    return None
