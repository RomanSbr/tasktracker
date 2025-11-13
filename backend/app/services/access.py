from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID

from app.models.project import Project
from app.models.task import Task
from app.models.organization import Organization
from app.models.associations import project_members, user_organizations


async def ensure_org_member(
    db: AsyncSession,
    *,
    organization_id: UUID,
    user_id: UUID,
    allowed_roles: Optional[List[str]] = None
) -> str:
    """Ensure user is member of organization (optionally with specific role)."""
    org = await db.get(Organization, organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    if org.owner_id == user_id:
        return "owner"

    query = select(
        user_organizations.c.role
    ).where(
        user_organizations.c.organization_id == organization_id,
        user_organizations.c.user_id == user_id,
    )
    result = await db.execute(query)
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a member of this organization",
        )

    if allowed_roles and role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions for this organization",
        )

    return role


async def ensure_project_access(
    db: AsyncSession,
    *,
    project_id: UUID,
    user_id: UUID
) -> Project:
    """Ensure user has access to project and return project."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.created_by == user_id:
        return project

    membership_query = select(project_members.c.project_id).where(
        project_members.c.project_id == project_id,
        project_members.c.user_id == user_id,
    )
    membership = await db.execute(membership_query)
    if membership.scalar_one_or_none():
        return project

    try:
        await ensure_org_member(db, organization_id=project.organization_id, user_id=user_id)
        return project
    except HTTPException:
        pass

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions for this project",
    )


async def ensure_task_access(
    db: AsyncSession,
    *,
    task_id: UUID,
    user_id: UUID
) -> Task:
    """Ensure user has access to task via its project membership."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await ensure_project_access(db, project_id=task.project_id, user_id=user_id)
    return task
