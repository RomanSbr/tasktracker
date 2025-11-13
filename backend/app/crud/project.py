from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.associations import project_members


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    async def get_by_key(self, db: AsyncSession, *, key: str) -> Optional[Project]:
        """Get project by key"""
        result = await db.execute(select(Project).where(Project.key == key))
        return result.scalar_one_or_none()

    async def get_by_organization(
        self, db: AsyncSession, *, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """Get projects by organization"""
        query = (
            select(Project)
            .where(Project.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_for_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        organization_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """Return projects accessible to user (creator or member)."""
        query = (
            select(Project)
            .outerjoin(project_members, project_members.c.project_id == Project.id)
            .where(
                or_(
                    Project.created_by == user_id,
                    project_members.c.user_id == user_id
                )
            )
        )

        if organization_id:
            query = query.where(Project.organization_id == organization_id)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().unique().all()

    async def add_member(
        self,
        db: AsyncSession,
        *,
        project_id: UUID,
        user_id: UUID,
        role: str = "member"
    ) -> None:
        """Add user to project members (idempotent)."""
        stmt = (
            insert(project_members)
            .values(project_id=project_id, user_id=user_id, role=role)
            .on_conflict_do_nothing()
        )
        await db.execute(stmt)


project = CRUDProject(Project)
