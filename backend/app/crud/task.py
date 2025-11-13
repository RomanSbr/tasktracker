from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.task import Task, TaskHistory
from app.models.project import Project
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.associations import project_members


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def get_by_project(
        self,
        db: AsyncSession,
        *,
        project_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Task]:
        """Get tasks by project ID"""
        query = select(Task).where(Task.project_id == project_id)

        if status:
            query = query.where(Task.status == status)

        query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()

    async def get_for_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict] = None
    ) -> List[Task]:
        """Get tasks available to a specific user (assignee, reporter, or project member)."""
        project_ids_subquery = select(project_members.c.project_id).where(
            project_members.c.user_id == user_id
        )

        query = select(Task).where(
            or_(
                Task.assignee_id == user_id,
                Task.reporter_id == user_id,
                Task.project_id.in_(project_ids_subquery)
            )
        )

        if filters:
            for key, value in filters.items():
                if hasattr(Task, key) and value is not None:
                    query = query.where(getattr(Task, key) == value)

        query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()

    async def get_next_task_number(self, db: AsyncSession, *, project_id: UUID) -> int:
        """Get next task number for project"""
        project_result = await db.execute(
            select(Project).where(Project.id == project_id).with_for_update()
        )
        project = project_result.scalar_one()
        project.key_sequence = (project.key_sequence or 0) + 1
        await db.flush()
        return project.key_sequence

    async def create_with_number(
        self, db: AsyncSession, *, obj_in: TaskCreate, reporter_id: UUID
    ) -> Task:
        """Create task with auto-generated task number"""
        task_number = await self.get_next_task_number(db, project_id=obj_in.project_id)

        obj_in_data = obj_in.model_dump()
        obj_in_data["task_number"] = task_number
        obj_in_data["reporter_id"] = reporter_id

        db_obj = Task(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def add_history(
        self,
        db: AsyncSession,
        *,
        task_id: UUID,
        user_id: UUID,
        action: str,
        field_name: Optional[str] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None
    ) -> TaskHistory:
        """Add history record for task"""
        history = TaskHistory(
            task_id=task_id,
            user_id=user_id,
            action=action,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value
        )
        db.add(history)
        await db.flush()
        return history

    async def update_positions(
        self,
        db: AsyncSession,
        *,
        task_positions: List[dict]
    ) -> None:
        """Update positions for multiple tasks (for backlog ordering)"""
        for item in task_positions:
            task_id = item.get("task_id")
            position = item.get("position")
            if task_id and position is not None:
                task = await self.get(db, id=task_id)
                if task:
                    task.position = position
                    db.add(task)
        await db.flush()

    async def get_backlog_tasks(
        self,
        db: AsyncSession,
        *,
        project_id: UUID,
        sprint_id: Optional[UUID] = None
    ) -> List[Task]:
        """Get backlog tasks (not in sprint or in specific sprint) ordered by position"""
        query = select(Task).where(Task.project_id == project_id)

        if sprint_id:
            query = query.where(Task.sprint_id == sprint_id)
        else:
            query = query.where(Task.sprint_id.is_(None))

        query = query.order_by(Task.position.asc(), Task.created_at.asc())
        result = await db.execute(query)
        return result.scalars().all()


task = CRUDTask(Task)
