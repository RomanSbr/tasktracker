from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.crud.permission_scheme import permission_scheme as crud_permission_scheme
from app.schemas.permission_scheme import (
    PermissionSchemeCreate,
    PermissionSchemeUpdate,
    PermissionSchemeResponse,
    PermissionSchemeRuleCreate,
    PermissionSchemeRuleUpdate,
    PermissionSchemeRuleResponse,
)
from app.models.user import User
from app.services.access import ensure_org_member

router = APIRouter()


@router.get("/organizations/{organization_id}/permission-schemes", response_model=List[PermissionSchemeResponse])
async def list_permission_schemes(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await ensure_org_member(db, organization_id=organization_id, user_id=current_user.id)
    schemes = await crud_permission_scheme.get_by_org(db, organization_id=organization_id)
    return schemes


@router.post("/organizations/{organization_id}/permission-schemes", response_model=PermissionSchemeResponse, status_code=status.HTTP_201_CREATED)
async def create_permission_scheme(
    organization_id: UUID,
    scheme_in: PermissionSchemeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if scheme_in.organization_id != organization_id:
        raise HTTPException(status_code=400, detail="Organization mismatch")

    role = await ensure_org_member(db, organization_id=organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    scheme = await crud_permission_scheme.create_with_rules(db, obj_in=scheme_in)
    await db.commit()
    await db.refresh(scheme)
    return scheme


@router.patch("/permission-schemes/{scheme_id}", response_model=PermissionSchemeResponse)
async def update_permission_scheme(
    scheme_id: UUID,
    scheme_in: PermissionSchemeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scheme = await crud_permission_scheme.get(db, id=scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Permission scheme not found")

    role = await ensure_org_member(db, organization_id=scheme.organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    updated = await crud_permission_scheme.update(db, db_obj=scheme, obj_in=scheme_in)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.post("/permission-schemes/{scheme_id}/rules", response_model=PermissionSchemeRuleResponse, status_code=status.HTTP_201_CREATED)
async def add_rule(
    scheme_id: UUID,
    rule_in: PermissionSchemeRuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scheme = await crud_permission_scheme.get(db, id=scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Permission scheme not found")

    role = await ensure_org_member(db, organization_id=scheme.organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    rule = await crud_permission_scheme.add_rule(db, scheme=scheme, rule_in=rule_in)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.patch("/permission-schemes/{scheme_id}/rules/{rule_id}", response_model=PermissionSchemeRuleResponse)
async def update_rule(
    scheme_id: UUID,
    rule_id: UUID,
    rule_in: PermissionSchemeRuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scheme = await crud_permission_scheme.get(db, id=scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Permission scheme not found")

    role = await ensure_org_member(db, organization_id=scheme.organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    rule = next((r for r in scheme.rules if r.id == rule_id), None)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    updated = await crud_permission_scheme.update_rule(db, rule=rule, rule_in=rule_in)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/permission-schemes/{scheme_id}/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(
    scheme_id: UUID,
    rule_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scheme = await crud_permission_scheme.get(db, id=scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Permission scheme not found")

    role = await ensure_org_member(db, organization_id=scheme.organization_id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await crud_permission_scheme.delete_rule(db, rule_id=rule_id)
    await db.commit()
    return None
