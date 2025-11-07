from sqlalchemy import Column, String, Text, ForeignKey, Integer, Float, DateTime, ARRAY, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), index=True)
    sprint_id = Column(UUID(as_uuid=True), ForeignKey("sprints.id", ondelete="SET NULL"), index=True)
    task_number = Column(Integer, nullable=False)

    # Main fields
    title = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="backlog", index=True)
    priority = Column(String(20), default="medium")
    type = Column(String(50), default="task")

    # Users
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Time and estimates
    due_date = Column(DateTime(timezone=True))
    estimated_hours = Column(Float)
    logged_hours = Column(Float, default=0)
    story_points = Column(Integer)

    # Additional fields
    tags = Column(ARRAY(String))
    custom_fields = Column(JSONB, default={})
    position = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True))
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assignee_id], back_populates="assigned_tasks")
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="reported_tasks")
    parent_task = relationship("Task", remote_side=[id], back_populates="subtasks")
    subtasks = relationship("Task", back_populates="parent_task")
    sprint = relationship("Sprint", back_populates="tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")
    history = relationship("TaskHistory", back_populates="task", cascade="all, delete-orphan")
    watchers = relationship("User", secondary="task_watchers", back_populates="watched_tasks")

    __table_args__ = (
        Index("idx_task_project_number", "project_id", "task_number", unique=True),
    )


class TaskHistory(Base):
    __tablename__ = "task_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String(50), nullable=False)
    field_name = Column(String(100))
    old_value = Column(Text)
    new_value = Column(Text)
    metadata = Column(JSONB, default={})

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    task = relationship("Task", back_populates="history")


class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    depends_on_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    dependency_type = Column(String(50), default="blocks")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
