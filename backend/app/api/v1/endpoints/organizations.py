from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_user
from app.crud.organization import organization as crud_organization
from app.crud.user import user as crud_user
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    OrganizationMemberResponse,
    OrganizationMemberAdd,
)
from app.schemas.user import UserResponseCompact
from app.models.user import User
from app.services.access import ensure_org_member

router = APIRouter()


@router.get("", response_model=List[OrganizationResponse])
async def list_organizations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List organizations available to user."""
    organizations = await crud_organization.get_for_user(db, user_id=current_user.id)
    return organizations


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_in: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new organization and seed defaults."""
    existing = await crud_organization.get_by_slug(db, slug=org_in.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Organization with this slug already exists")

    organization = await crud_organization.create_with_owner(
        db,
        owner_id=current_user.id,
        obj_in=org_in
    )
    await db.commit()
    await db.refresh(organization)
    return organization


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get organization details."""
    organization = await crud_organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    await ensure_org_member(db, organization_id=organization.id, user_id=current_user.id)
    return organization


@router.patch("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: UUID,
    org_in: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update organization (owner/admin only)."""
    organization = await crud_organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    role = await ensure_org_member(
        db,
        organization_id=organization.id,
        user_id=current_user.id
    )
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    organization = await crud_organization.update(db, db_obj=organization, obj_in=org_in)
    await db.commit()
    await db.refresh(organization)
    return organization


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete organization (owner only)."""
    organization = await crud_organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    role = await ensure_org_member(
        db,
        organization_id=organization.id,
        user_id=current_user.id
    )
    if role != "owner":
        raise HTTPException(status_code=403, detail="Only owner can delete organization")

    await crud_organization.delete(db, id=organization.id)
    await db.commit()
    return None


@router.get("/{organization_id}/members", response_model=List[OrganizationMemberResponse])
async def list_members(
    organization_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List organization members."""
    await ensure_org_member(db, organization_id=organization_id, user_id=current_user.id)
    rows = await crud_organization.get_members(db, organization_id=organization_id)

    members: List[OrganizationMemberResponse] = []
    for row in rows:
        user: User = row[4]
        members.append(
            OrganizationMemberResponse(
                user=UserResponseCompact(
                    id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    avatar_url=user.avatar_url,
                ),
                role=row[1],
                permissions=row[2] or {},
                joined_at=row[3],
            )
        )
    return members


@router.post("/{organization_id}/members", status_code=status.HTTP_204_NO_CONTENT)
async def add_member(
    organization_id: UUID,
    member_in: OrganizationMemberAdd,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add member to organization."""
    organization = await crud_organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    role = await ensure_org_member(db, organization_id=organization.id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    target_user = await crud_user.get(db, id=member_in.user_id)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    await crud_organization.add_member(
        db,
        organization_id=organization.id,
        user_id=member_in.user_id,
        role=member_in.role,
        permissions=member_in.permissions,
    )
    await db.commit()
    return None


@router.delete("/{organization_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    organization_id: UUID,
    member_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove member from organization."""
    organization = await crud_organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    role = await ensure_org_member(db, organization_id=organization.id, user_id=current_user.id)
    if role not in {"owner", "admin"}:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    await crud_organization.remove_member(
        db,
        organization_id=organization.id,
        user_id=member_id,
    )
    await db.commit()
    return None
