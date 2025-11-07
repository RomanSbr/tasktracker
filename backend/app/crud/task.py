from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.task import Task, TaskHistory
from app.schemas.task import TaskCreate, TaskUpdate


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

    async def get_next_task_number(self, db: AsyncSession, *, project_id: UUID) -> int:
        """Get next task number for project"""
        result = await db.execute(
            select(func.max(Task.task_number)).where(Task.project_id == project_id)
        )
        max_number = result.scalar()
        return (max_number or 0) + 1

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


task = CRUDTask(Task)
