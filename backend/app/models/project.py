from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    key = Column(String(10), unique=True, nullable=False, index=True)
    description = Column(Text)
    status = Column(String(50), default="active")
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Numeric(15, 2))
    settings = Column(JSONB, default={})
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    archived_at = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    organization = relationship("Organization", back_populates="projects")
    members = relationship("User", secondary="project_members", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    sprints = relationship("Sprint", back_populates="project", cascade="all, delete-orphan")
