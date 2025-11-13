from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.organization import Organization
from app.models.permission import PermissionScheme, PermissionSchemeRule
from app.models.workflow import Workflow, WorkflowStatus, WorkflowTransition
from app.models.user import User
from app.models.associations import user_organizations
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


DEFAULT_STATUSES = [
    {"key": "backlog", "name": "Backlog", "category": "todo"},
    {"key": "todo", "name": "To Do", "category": "todo"},
    {"key": "in_progress", "name": "In Progress", "category": "in_progress"},
    {"key": "review", "name": "Review", "category": "in_progress"},
    {"key": "testing", "name": "Testing", "category": "in_progress"},
    {"key": "done", "name": "Done", "category": "done"},
]

DEFAULT_PERMISSIONS = [
    ("BROWSE_PROJECTS", "role", "viewer"),
    ("VIEW_ISSUES", "role", "viewer"),
    ("CREATE_ISSUES", "role", "member"),
    ("EDIT_ISSUES", "role", "developer"),
    ("TRANSITION_ISSUES", "role", "developer"),
    ("MANAGE_SPRINTS", "role", "lead"),
    ("ADMINISTER_PROJECT", "role", "lead"),
]


class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):
    async def get_by_slug(self, db: AsyncSession, *, slug: str) -> Optional[Organization]:
        result = await db.execute(select(Organization).where(Organization.slug == slug))
        return result.scalar_one_or_none()

    async def get_for_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID
    ) -> List[Organization]:
        query = (
            select(Organization)
            .outerjoin(user_organizations, user_organizations.c.organization_id == Organization.id)
            .where(
                (Organization.owner_id == user_id) |
                (user_organizations.c.user_id == user_id)
            )
            .order_by(Organization.created_at.desc())
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

    async def create_with_owner(
        self,
        db: AsyncSession,
        *,
        owner_id: UUID,
        obj_in: OrganizationCreate
    ) -> Organization:
        data = obj_in.model_dump()
        data["owner_id"] = owner_id
        org = Organization(**data)
        db.add(org)
        await db.flush()

        await db.execute(
            insert(user_organizations)
            .values(
                user_id=owner_id,
                organization_id=org.id,
                role="owner",
                permissions={}
            )
            .on_conflict_do_nothing()
        )

        workflow = Workflow(
            organization_id=org.id,
            name="Software Simplified",
            type="software",
            is_default=True,
        )
        db.add(workflow)
        await db.flush()

        status_entities = []
        for order, status in enumerate(DEFAULT_STATUSES):
            status_entities.append(
                WorkflowStatus(
                    workflow_id=workflow.id,
                    key=status["key"],
                    name=status["name"],
                    order=order,
                    category=status["category"],
                )
            )
        db.add_all(status_entities)
        await db.flush()

        transitions = []
        for index in range(len(status_entities) - 1):
            transitions.append(
                WorkflowTransition(
                    workflow_id=workflow.id,
                    from_status_id=status_entities[index].id,
                    to_status_id=status_entities[index + 1].id,
                    allowed_roles=["lead", "developer"],
                )
            )
        db.add_all(transitions)

        scheme = PermissionScheme(
            organization_id=org.id,
            name="Default scheme",
            description="Auto generated defaults",
        )
        db.add(scheme)
        await db.flush()

        rules = [
            PermissionSchemeRule(
                scheme_id=scheme.id,
                permission_key=perm,
                principal_type=ptype,
                principal_identifier=identifier,
            )
            for perm, ptype, identifier in DEFAULT_PERMISSIONS
        ]
        db.add_all(rules)

        await db.flush()
        await db.refresh(org)
        return org

    async def get_members(self, db: AsyncSession, *, organization_id: UUID):
        query = (
            select(
                user_organizations.c.user_id,
                user_organizations.c.role,
                user_organizations.c.permissions,
                user_organizations.c.joined_at,
                User
            )
            .join(User, User.id == user_organizations.c.user_id)
            .where(user_organizations.c.organization_id == organization_id)
            .order_by(user_organizations.c.joined_at.asc())
        )
        result = await db.execute(query)
        return result.all()

    async def add_member(
        self,
        db: AsyncSession,
        *,
        organization_id: UUID,
        user_id: UUID,
        role: str,
        permissions: Optional[dict] = None
    ) -> None:
        stmt = (
            insert(user_organizations)
            .values(
                organization_id=organization_id,
                user_id=user_id,
                role=role,
                permissions=permissions or {},
            )
            .on_conflict_do_nothing()
        )
        await db.execute(stmt)

    async def remove_member(
        self,
        db: AsyncSession,
        *,
        organization_id: UUID,
        user_id: UUID
    ) -> None:
        stmt = (
            delete(user_organizations)
            .where(
                user_organizations.c.organization_id == organization_id,
                user_organizations.c.user_id == user_id,
            )
        )
        await db.execute(stmt)


organization = CRUDOrganization(Organization)
