from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.api.deps import get_db, get_current_user
from app.crud.workflow import workflow as crud_workflow
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowStatusCreate,
    WorkflowStatusUpdate,
    WorkflowStatusResponse,
)
from app.models.user import User
from app.services.access import ensure_org_member

router = APIRouter()


@router.get("/organizations/{organization_id}/workflows", response_model=List[WorkflowResponse])
async def list_workflows(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await ensure_org_member(db, organization_id=organization_id, user_id=current_user.id)
    workflows = await crud_workflow.get_by_org(db, organization_id=organization_id)
    return workflows


@router.post("/organizations/{organization_id}/workflows", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    organization_id: UUID,
    workflow_in: WorkflowCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if workflow_in.organization_id != organization_id:
        raise HTTPException(status_code=400, detail="Organization mismatch")

    role = await ensure_org_member(db, organization_id=organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow = await crud_workflow.create_with_statuses(db, obj_in=workflow_in)
    await db.commit()
    await db.refresh(workflow)
    return workflow


@router.patch("/workflows/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: UUID,
    workflow_in: WorkflowUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = await crud_workflow.get(db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    role = await ensure_org_member(db, organization_id=workflow.organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    updated = await crud_workflow.update(db, db_obj=workflow, obj_in=workflow_in)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.post("/workflows/{workflow_id}/statuses", response_model=WorkflowStatusResponse, status_code=status.HTTP_201_CREATED)
async def add_status(
    workflow_id: UUID,
    status_in: WorkflowStatusCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = await crud_workflow.get(db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    role = await ensure_org_member(db, organization_id=workflow.organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    status_obj = await crud_workflow.add_status(db, workflow=workflow, status_in=status_in)
    await db.commit()
    await db.refresh(status_obj)
    return status_obj


@router.patch("/workflows/{workflow_id}/statuses/{status_id}", response_model=WorkflowStatusResponse)
async def update_status(
    workflow_id: UUID,
    status_id: UUID,
    status_in: WorkflowStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = await crud_workflow.get(db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    role = await ensure_org_member(db, organization_id=workflow.organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    status_obj = next((s for s in workflow.statuses if s.id == status_id), None)
    if not status_obj:
        raise HTTPException(status_code=404, detail="Status not found")

    updated = await crud_workflow.update_status(db, status=status_obj, status_in=status_in)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/workflows/{workflow_id}/statuses/{status_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_status(
    workflow_id: UUID,
    status_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    workflow = await crud_workflow.get(db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    role = await ensure_org_member(db, organization_id=workflow.organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await crud_workflow.delete_status(db, status_id=status_id)
    await db.commit()
    return None
