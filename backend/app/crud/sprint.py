from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.sprint import Sprint
from app.models.task import Task
from app.schemas.sprint import SprintCreate, SprintUpdate


class CRUDSprint(CRUDBase[Sprint, SprintCreate, SprintUpdate]):
    async def get_by_project(
        self,
        db: AsyncSession,
        *,
        project_id: UUID,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Sprint]:
        """Get sprints by project ID"""
        query = select(Sprint).where(Sprint.project_id == project_id)

        if status:
            query = query.where(Sprint.status == status)

        query = query.order_by(Sprint.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_active(self, db: AsyncSession, *, project_id: UUID) -> Optional[Sprint]:
        """Get active sprint for project"""
        result = await db.execute(
            select(Sprint)
            .where(
                and_(
                    Sprint.project_id == project_id,
                    Sprint.status == "active"
                )
            )
            .order_by(Sprint.start_date.desc())
        )
        return result.scalar_one_or_none()

    async def get_next_sprint_number(self, db: AsyncSession, *, project_id: UUID) -> int:
        """Get next sprint number for project"""
        result = await db.execute(
            select(func.max(Sprint.sprint_number))
            .where(Sprint.project_id == project_id)
        )
        max_number = result.scalar()
        return (max_number or 0) + 1

    async def create(self, db: AsyncSession, *, obj_in: SprintCreate) -> Sprint:
        """Create new sprint with auto-generated sprint number"""
        sprint_number = await self.get_next_sprint_number(db, project_id=obj_in.project_id)

        obj_in_data = obj_in.model_dump()
        obj_in_data["sprint_number"] = sprint_number
        obj_in_data["status"] = "planned"

        db_obj = Sprint(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def start(self, db: AsyncSession, *, sprint: Sprint, start_date: Optional[datetime] = None) -> Sprint:
        """Start sprint"""
        sprint.status = "active"
        if start_date:
            sprint.start_date = start_date
        elif not sprint.start_date:
            sprint.start_date = datetime.utcnow()

        db.add(sprint)
        await db.flush()
        await db.refresh(sprint)
        return sprint

    async def complete(self, db: AsyncSession, *, sprint: Sprint) -> Sprint:
        """Complete sprint"""
        sprint.status = "completed"
        sprint.completed_at = datetime.utcnow()

        db.add(sprint)
        await db.flush()
        await db.refresh(sprint)
        return sprint

    async def get_stats(self, db: AsyncSession, *, sprint_id: UUID) -> dict:
        """Get sprint statistics"""
        tasks_query = select(
            func.count(Task.id).label("total"),
            func.sum(Task.story_points).label("total_points"),
            func.sum(
                func.case((Task.status == "done", Task.story_points), else_=0)
            ).label("completed_points")
        ).where(Task.sprint_id == sprint_id)

        result = await db.execute(tasks_query)
        row = result.first()

        completed_query = select(func.count(Task.id)).where(
            and_(Task.sprint_id == sprint_id, Task.status == "done")
        )
        completed_result = await db.execute(completed_query)
        completed_count = completed_result.scalar() or 0

        return {
            "tasks_count": row.total or 0,
            "completed_tasks_count": completed_count,
            "total_story_points": row.total_points or 0,
            "completed_story_points": row.completed_points or 0,
        }


sprint = CRUDSprint(Sprint)

