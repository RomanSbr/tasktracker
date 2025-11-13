from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.workflow import Workflow, WorkflowStatus
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowStatusCreate, WorkflowStatusUpdate


class CRUDWorkflow(CRUDBase[Workflow, WorkflowCreate, WorkflowUpdate]):
    async def get_by_org(self, db: AsyncSession, *, organization_id: UUID) -> List[Workflow]:
        result = await db.execute(
            select(Workflow).where(Workflow.organization_id == organization_id).order_by(Workflow.created_at.desc())
        )
        return result.scalars().unique().all()

    async def create_with_statuses(self, db: AsyncSession, *, obj_in: WorkflowCreate) -> Workflow:
        data = obj_in.model_dump(exclude={"statuses"})
        statuses_data = obj_in.statuses
        workflow = Workflow(**data)
        db.add(workflow)
        await db.flush()

        for index, status in enumerate(statuses_data):
            db.add(
                WorkflowStatus(
                    workflow_id=workflow.id,
                    key=status.key,
                    name=status.name,
                    order=status.order or index,
                    category=status.category,
                )
            )

        await db.flush()
        await db.refresh(workflow)
        return workflow

    async def add_status(
        self,
        db: AsyncSession,
        *,
        workflow: Workflow,
        status_in: WorkflowStatusCreate
    ) -> WorkflowStatus:
        status = WorkflowStatus(
            workflow_id=workflow.id,
            key=status_in.key,
            name=status_in.name,
            order=status_in.order,
            category=status_in.category,
        )
        db.add(status)
        await db.flush()
        await db.refresh(status)
        return status

    async def update_status(
        self,
        db: AsyncSession,
        *,
        status: WorkflowStatus,
        status_in: WorkflowStatusUpdate
    ) -> WorkflowStatus:
        update_data = status_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(status, field, value)
        db.add(status)
        await db.flush()
        await db.refresh(status)
        return status

    async def delete_status(self, db: AsyncSession, *, status_id: UUID) -> None:
        await db.execute(delete(WorkflowStatus).where(WorkflowStatus.id == status_id))


workflow = CRUDWorkflow(Workflow)
