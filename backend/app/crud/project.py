from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    async def get_by_key(self, db: AsyncSession, *, key: str) -> Optional[Project]:
        """Get project by key"""
        result = await db.execute(select(Project).where(Project.key == key))
        return result.scalar_one_or_none()

    async def get_by_organization(
        self, db: AsyncSession, *, organization_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Project]:
        """Get projects by organization"""
        query = (
            select(Project)
            .where(Project.organization_id == organization_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()


project = CRUDProject(Project)
