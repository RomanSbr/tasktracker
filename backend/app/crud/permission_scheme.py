from typing import List
from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.permission import PermissionScheme, PermissionSchemeRule
from app.schemas.permission_scheme import (
    PermissionSchemeCreate,
    PermissionSchemeUpdate,
    PermissionSchemeRuleCreate,
    PermissionSchemeRuleUpdate,
)


class CRUDPermissionScheme(CRUDBase[PermissionScheme, PermissionSchemeCreate, PermissionSchemeUpdate]):
    async def get_by_org(self, db: AsyncSession, *, organization_id: UUID) -> List[PermissionScheme]:
        result = await db.execute(
            select(PermissionScheme)
            .where(PermissionScheme.organization_id == organization_id)
            .order_by(PermissionScheme.created_at.desc())
        )
        return result.scalars().unique().all()

    async def create_with_rules(self, db: AsyncSession, *, obj_in: PermissionSchemeCreate) -> PermissionScheme:
        data = obj_in.model_dump(exclude={"rules"})
        rules_data = obj_in.rules
        scheme = PermissionScheme(**data)
        db.add(scheme)
        await db.flush()

        for rule in rules_data:
            db.add(
                PermissionSchemeRule(
                    scheme_id=scheme.id,
                    permission_key=rule.permission_key,
                    principal_type=rule.principal_type,
                    principal_identifier=rule.principal_identifier,
                    constraints=rule.constraints or {},
                )
            )

        await db.flush()
        await db.refresh(scheme)
        return scheme

    async def add_rule(
        self,
        db: AsyncSession,
        *,
        scheme: PermissionScheme,
        rule_in: PermissionSchemeRuleCreate
    ) -> PermissionSchemeRule:
        rule = PermissionSchemeRule(
            scheme_id=scheme.id,
            permission_key=rule_in.permission_key,
            principal_type=rule_in.principal_type,
            principal_identifier=rule_in.principal_identifier,
            constraints=rule_in.constraints or {},
        )
        db.add(rule)
        await db.flush()
        await db.refresh(rule)
        return rule

    async def update_rule(
        self,
        db: AsyncSession,
        *,
        rule: PermissionSchemeRule,
        rule_in: PermissionSchemeRuleUpdate
    ) -> PermissionSchemeRule:
        update_data = rule_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(rule, field, value)
        db.add(rule)
        await db.flush()
        await db.refresh(rule)
        return rule

    async def delete_rule(self, db: AsyncSession, *, rule_id: UUID) -> None:
        await db.execute(delete(PermissionSchemeRule).where(PermissionSchemeRule.id == rule_id))


permission_scheme = CRUDPermissionScheme(PermissionScheme)
