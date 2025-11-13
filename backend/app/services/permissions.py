from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID

from app.models.project import Project
from app.models.permission import PermissionScheme, PermissionSchemeRule
from app.models.associations import project_members, user_organizations
from app.services.access import ensure_project_access, ensure_org_member


async def check_project_permission(
    db: AsyncSession,
    *,
    project_id: UUID,
    user_id: UUID,
    permission_key: str
) -> bool:
    """Check if user has specific permission for project."""
    project = await ensure_project_access(db, project_id=project_id, user_id=user_id)
    
    if not project.permission_scheme_id:
        # Fallback: use role-based permissions
        return await _check_role_based_permission(
            db,
            project_id=project_id,
            user_id=user_id,
            permission_key=permission_key
        )
    
    # Get permission scheme
    scheme = await db.get(PermissionScheme, project.permission_scheme_id)
    if not scheme:
        return await _check_role_based_permission(
            db,
            project_id=project_id,
            user_id=user_id,
            permission_key=permission_key
        )
    
    # Get user's role in project
    project_role = await _get_project_role(db, project_id=project_id, user_id=user_id)
    org_role = await _get_org_role(db, organization_id=project.organization_id, user_id=user_id)
    
    # Check permission scheme rules
    rules_query = select(PermissionSchemeRule).where(
        PermissionSchemeRule.scheme_id == scheme.id,
        PermissionSchemeRule.permission_key == permission_key
    )
    rules_result = await db.execute(rules_query)
    rules = rules_result.scalars().all()
    
    for rule in rules:
        if rule.principal_type == "role":
            if rule.principal_identifier == project_role or rule.principal_identifier == org_role:
                return True
        elif rule.principal_type == "user":
            if rule.principal_identifier == str(user_id):
                return True
    
    # Fallback to role-based
    return await _check_role_based_permission(
        db,
        project_id=project_id,
        user_id=user_id,
        permission_key=permission_key
    )


async def require_project_permission(
    db: AsyncSession,
    *,
    project_id: UUID,
    user_id: UUID,
    permission_key: str
) -> Project:
    """Require specific permission for project, raise 403 if not allowed."""
    has_permission = await check_project_permission(
        db,
        project_id=project_id,
        user_id=user_id,
        permission_key=permission_key
    )
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission '{permission_key}' required"
        )
    
    return await ensure_project_access(db, project_id=project_id, user_id=user_id)


async def _get_project_role(
    db: AsyncSession,
    *,
    project_id: UUID,
    user_id: UUID
) -> Optional[str]:
    """Get user's role in project."""
    query = select(project_members.c.role).where(
        project_members.c.project_id == project_id,
        project_members.c.user_id == user_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def _get_org_role(
    db: AsyncSession,
    *,
    organization_id: UUID,
    user_id: UUID
) -> Optional[str]:
    """Get user's role in organization."""
    from app.models.organization import Organization
    
    org = await db.get(Organization, organization_id)
    if org and org.owner_id == user_id:
        return "owner"
    
    query = select(user_organizations.c.role).where(
        user_organizations.c.organization_id == organization_id,
        user_organizations.c.user_id == user_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def _check_role_based_permission(
    db: AsyncSession,
    *,
    project_id: UUID,
    user_id: UUID,
    permission_key: str
) -> bool:
    """Fallback role-based permission check."""
    project = await db.get(Project, project_id)
    if not project:
        return False
    
    # Get roles
    project_role = await _get_project_role(db, project_id=project_id, user_id=user_id)
    org_role = await _get_org_role(db, organization_id=project.organization_id, user_id=user_id)
    
    # Default permission mappings
    permission_mappings = {
        "BROWSE_PROJECTS": ["owner", "admin", "member", "viewer", "lead", "developer", "guest"],
        "VIEW_ISSUES": ["owner", "admin", "member", "viewer", "lead", "developer", "guest"],
        "CREATE_ISSUES": ["owner", "admin", "member", "lead", "developer"],
        "EDIT_ISSUES": ["owner", "admin", "member", "lead", "developer"],
        "TRANSITION_ISSUES": ["owner", "admin", "member", "lead", "developer"],
        "MANAGE_SPRINTS": ["owner", "admin", "lead"],
        "ADMINISTER_PROJECT": ["owner", "admin", "lead"],
        "COMMENT": ["owner", "admin", "member", "viewer", "lead", "developer"],
        "DELETE_COMMENT": ["owner", "admin", "lead", "developer"],
    }
    
    allowed_roles = permission_mappings.get(permission_key, [])
    
    # Check project role first, then org role
    if project_role and project_role in allowed_roles:
        return True
    if org_role and org_role in allowed_roles:
        return True
    
    return False

