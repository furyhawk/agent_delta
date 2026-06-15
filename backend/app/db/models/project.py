"""Project and ProjectMember models for multi-user project management (SQLModel)."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import Field, Relationship, SQLModel

from app.db.base import TimestampMixin


class Project(TimestampMixin, SQLModel, table=True):
    """Project model — represents an isolated workspace (Docker volume + container).

    Each project has a stable container_name and volume_name generated at creation.
    The Docker container is started lazily on first chat within the project.
    """

    __tablename__ = "projects"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True),
    )
    owner_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
    )
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
    image: str = Field(default="python:3.12-slim", max_length=255)
    # Stable Docker identifiers — pd-{id} and pd-vol-{id}
    container_name: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False),
    )
    volume_name: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False),
    )
    archived_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True),
    )

    # Relationships
    members: list["ProjectMember"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name={self.name})>"


class ProjectMember(SQLModel, table=True):
    """ProjectMember — role-based membership in a project.

    Roles: viewer (read-only), editor (read + write chats), admin (invite + manage).
    The project owner has implicit full access and is not in this table.
    """

    __tablename__ = "project_members"

    project_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("projects.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )
    role: str = Field(default="viewer", max_length=20)  # viewer | editor | admin
    invited_by: uuid.UUID | None = Field(
        default=None,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("users.id"),
            nullable=True,
        ),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    # Relationship
    project: "Project" = Relationship(back_populates="members")

    def __repr__(self) -> str:
        return f"<ProjectMember(project_id={self.project_id}, user_id={self.user_id}, role={self.role})>"
