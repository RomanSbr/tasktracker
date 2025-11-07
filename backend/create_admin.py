"""Script to create admin user"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.crud.user import user as crud_user
from app.schemas.user import UserCreate
# Import all models to avoid relationship errors
from app.db import base


async def create_admin():
    """Create admin user"""
    async with AsyncSessionLocal() as db:
        # Admin credentials
        admin_data = UserCreate(
            email="admin@tasktracker.com",
            username="admin",
            password="Admin123!",
            full_name="Administrator"
        )

        # Check if admin already exists
        existing_user = await crud_user.get_by_email(db, email=admin_data.email)
        if existing_user:
            print("❌ Admin user already exists!")
            print(f"Email: {admin_data.email}")
            print(f"Username: {admin_data.username}")
            return

        existing_user = await crud_user.get_by_username(db, username=admin_data.username)
        if existing_user:
            print("❌ User with username 'admin' already exists!")
            return

        # Create admin user
        user = await crud_user.create(db, obj_in=admin_data)
        await db.commit()

        print("✅ Admin user created successfully!")
        print(f"Email: {admin_data.email}")
        print(f"Username: {admin_data.username}")
        print(f"Password: {admin_data.password}")
        print(f"Full Name: {admin_data.full_name}")


if __name__ == "__main__":
    asyncio.run(create_admin())
