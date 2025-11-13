from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.session import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String(500))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    settings = Column(JSONB, default={})
    default_role = Column(String(50), nullable=False, default="member")

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    owner = relationship("User", back_populates="owned_organizations", foreign_keys=[owner_id])
    members = relationship("User", secondary="user_organizations", back_populates="organizations")
    projects = relationship("Project", back_populates="organization")
