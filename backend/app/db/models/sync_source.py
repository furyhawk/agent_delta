"""SyncSource model — stores RAG sync source configurations."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import Field, SQLModel

from app.db.base import TimestampMixin


class SyncSource(TimestampMixin, SQLModel, table=True):
    """Configurable connector source for RAG document synchronization."""

    __tablename__ = "sync_sources"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True),
    )
    name: str = Field(sa_column=Column(String(255), nullable=False))
    connector_type: str = Field(sa_column=Column(String(20), nullable=False))
    collection_name: str = Field(sa_column=Column(String(255), nullable=False, index=True))
    config: dict[str, object] = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=False, server_default="{}")
    )
    sync_mode: str = Field(
        default="new_only", sa_column=Column(String(20), nullable=False, default="new_only")
    )
    schedule_minutes: int | None = Field(default=None, sa_column=Column(Integer, nullable=True))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False, default=True))
    last_sync_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    last_sync_status: str | None = Field(default=None, sa_column=Column(String(20), nullable=True))
    last_error: str | None = Field(default=None, sa_column=Column(Text, nullable=True))
