"""User database model (SQLModel + PostgreSQL)."""

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import Field, SQLModel

from app.db.base import TimestampMixin


class UserRole(StrEnum):
    """User role enumeration.

    Roles hierarchy (higher includes lower permissions):
    - ADMIN: Full system access, can manage users and settings
    - USER: Standard user access
    """

    ADMIN = "admin"
    USER = "user"


class User(TimestampMixin, SQLModel, table=True):
    """User model."""

    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True),
    )
    email: str = Field(sa_column=Column(String(255), unique=True, index=True, nullable=False))
    hashed_password: str | None = Field(default=None, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool = Field(default=True, sa_column=Column(Boolean, default=True, nullable=False))
    role: str = Field(default=UserRole.USER.value, max_length=50)
    is_app_admin: bool = Field(
        default=False, sa_column=Column(Boolean, default=False, nullable=False)
    )
    avatar_url: str | None = Field(default=None, max_length=500)
    onboarding_completed_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    @property
    def user_role(self) -> UserRole:
        """Get role as enum."""
        return UserRole(self.role)

    def has_role(self, required_role: UserRole) -> bool:
        """Check if user has the required role or higher."""
        if self.role == UserRole.ADMIN.value:
            return True
        return self.role == required_role.value

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
