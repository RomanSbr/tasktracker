from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.api.deps import get_db, get_current_user
from sqlalchemy import select

from app.crud.project import project as crud_project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.models.user import User
from app.services.access import ensure_project_access, ensure_org_member
from app.services.permissions import require_project_permission
from app.models.workflow import Workflow, WorkflowStatus
from app.models.permission import PermissionScheme
from app.schemas.workflow import WorkflowResponse

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
    projects = await crud_project.get_for_user(
        db,
        user_id=current_user.id,
        organization_id=organization_id,
        skip=skip,
        limit=limit
    )
    return projects


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new project"""
    await ensure_org_member(
        db,
        organization_id=project_in.organization_id,
        user_id=current_user.id,
        allowed_roles=["owner", "admin"],
    )

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
    if not project_data.get("lead_id"):
        project_data["lead_id"] = current_user.id

    if not project_data.get("workflow_id"):
        workflow = await db.execute(
            select(Workflow)
            .where(Workflow.organization_id == project_data["organization_id"])
            .order_by(Workflow.is_default.desc(), Workflow.created_at.desc())
        )
        workflow_obj = workflow.scalars().first()
        if workflow_obj:
            project_data["workflow_id"] = workflow_obj.id

    if not project_data.get("permission_scheme_id"):
        scheme = await db.execute(
            select(PermissionScheme)
            .where(PermissionScheme.organization_id == project_data["organization_id"])
            .order_by(PermissionScheme.created_at.desc())
        )
        scheme_obj = scheme.scalars().first()
        if scheme_obj:
            project_data["permission_scheme_id"] = scheme_obj.id

    from app.schemas.project import ProjectCreate as PC
    project = await crud_project.create(
        db,
        obj_in=PC(**project_data)
    )

    await db.commit()
    await db.refresh(project)
    await crud_project.add_member(
        db,
        project_id=project.id,
        user_id=current_user.id,
        role="lead"
    )
    await db.commit()
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get project by ID"""
    project = await ensure_project_access(db, project_id=project_id, user_id=current_user.id)
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_in: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update project"""
    await require_project_permission(
        db,
        project_id=project_id,
        user_id=current_user.id,
        permission_key="ADMINISTER_PROJECT"
    )
    project = await ensure_project_access(db, project_id=project_id, user_id=current_user.id)

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
    await require_project_permission(
        db,
        project_id=project_id,
        user_id=current_user.id,
        permission_key="ADMINISTER_PROJECT"
    )
    await ensure_project_access(db, project_id=project_id, user_id=current_user.id)

    await crud_project.delete(db, id=project_id)
    await db.commit()
    return None


@router.get("/{project_id}/workflow", response_model=WorkflowResponse)
async def get_project_workflow(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get workflow for project"""
    project = await ensure_project_access(db, project_id=project_id, user_id=current_user.id)
    
    if not project.workflow_id:
        raise HTTPException(status_code=404, detail="Project has no workflow assigned")
    
    workflow = await db.get(Workflow, project.workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Load statuses
    statuses_result = await db.execute(
        select(WorkflowStatus)
        .where(WorkflowStatus.workflow_id == workflow.id)
        .order_by(WorkflowStatus.order.asc())
    )
    workflow.statuses = statuses_result.scalars().all()
    
    return workflow
