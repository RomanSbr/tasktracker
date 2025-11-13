from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), default="software")
    is_default = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    statuses = relationship("WorkflowStatus", back_populates="workflow", cascade="all, delete-orphan")
    transitions = relationship("WorkflowTransition", back_populates="workflow", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="workflow")


class WorkflowStatus(Base):
    __tablename__ = "workflow_statuses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False, default=0)
    category = Column(String(50), default="todo")

    workflow = relationship("Workflow", back_populates="statuses")


class WorkflowTransition(Base):
    __tablename__ = "workflow_transitions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False)
    from_status_id = Column(UUID(as_uuid=True), ForeignKey("workflow_statuses.id", ondelete="CASCADE"), nullable=False)
    to_status_id = Column(UUID(as_uuid=True), ForeignKey("workflow_statuses.id", ondelete="CASCADE"), nullable=False)
    allowed_roles = Column(ARRAY(String), default=[])

    workflow = relationship("Workflow", back_populates="transitions")
