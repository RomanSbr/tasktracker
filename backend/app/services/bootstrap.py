from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.crud.user import user as crud_user
from app.schemas.user import UserCreate


async def ensure_default_admin():
    """Ensure default admin user exists."""
    if not settings.DEFAULT_ADMIN_EMAIL or not settings.DEFAULT_ADMIN_PASSWORD:
        return

    async with AsyncSessionLocal() as db:
        existing = await crud_user.get_by_email(db, email=settings.DEFAULT_ADMIN_EMAIL)
        if not existing:
            user_in = UserCreate(
                email=settings.DEFAULT_ADMIN_EMAIL,
                username=settings.DEFAULT_ADMIN_USERNAME or settings.DEFAULT_ADMIN_EMAIL,
                password=settings.DEFAULT_ADMIN_PASSWORD,
                first_name=settings.DEFAULT_ADMIN_FIRST_NAME or "Admin",
                last_name=settings.DEFAULT_ADMIN_LAST_NAME or "User",
            )
            admin = await crud_user.create(db, obj_in=user_in)
            admin.is_superuser = True
            admin.is_verified = True
            db.add(admin)
        else:
            if not existing.is_superuser:
                existing.is_superuser = True
                db.add(existing)

        await db.commit()
