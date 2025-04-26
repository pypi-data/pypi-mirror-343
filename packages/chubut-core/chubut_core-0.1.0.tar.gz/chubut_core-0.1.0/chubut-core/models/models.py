from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlmodel import Column, DateTime, Field

class Identifiable(BaseModel):
    id: int = Field(None, primary_key=True, nullable=False)


class Auditable(BaseModel):
    """Helper for datetime value of when the entity was created and when it was last modified."""

    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: Optional[datetime] = Field(sa_column=Column(DateTime, onupdate=datetime.now, nullable=True))
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)
    updated_by: Optional[str] = Field(default=None, nullable=True)


class UUIDModel(BaseModel):
    uuid: Optional[UUID] = Field(default_factory=uuid4, nullable=False)