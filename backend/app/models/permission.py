from sqlalchemy import Column, String, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class PermissionScheme(Base):
    __tablename__ = "permission_schemes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    rules = relationship("PermissionSchemeRule", back_populates="scheme", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="permission_scheme")


class PermissionSchemeRule(Base):
    __tablename__ = "permission_scheme_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_id = Column(UUID(as_uuid=True), ForeignKey("permission_schemes.id", ondelete="CASCADE"), nullable=False)
    permission_key = Column(String(100), nullable=False)
    principal_type = Column(String(50), nullable=False)  # role, user, group и т.д.
    principal_identifier = Column(String(255), nullable=False)
    constraints = Column(JSONB, default={})

    scheme = relationship("PermissionScheme", back_populates="rules")
