from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base
from app.models.associations import project_members


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    bio = Column(Text)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    owned_organizations = relationship("Organization", back_populates="owner", foreign_keys="Organization.owner_id")
    organizations = relationship("Organization", secondary="user_organizations", back_populates="members")
    projects = relationship(
        "Project",
        secondary=project_members,
        back_populates="members",
        primaryjoin=id == project_members.c.user_id,
        secondaryjoin="Project.id == project_members.c.project_id",
    )
    assigned_tasks = relationship("Task", back_populates="assignee", foreign_keys="Task.assignee_id")
    reported_tasks = relationship("Task", back_populates="reporter", foreign_keys="Task.reporter_id")
    watched_tasks = relationship("Task", secondary="task_watchers", back_populates="watchers")
    comments = relationship("Comment", back_populates="user")

    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
