from datetime import datetime
from typing import Optional
from sqlalchemy import FunctionElement, DateTime
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import declarative_mixin
from sqlmodel import SQLModel, Field


class utcnow(FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        nullable=False,
        index=False,
        sa_column_kwargs={"server_default": utcnow()}
    )
    updated_at: Optional[datetime] = Field(
        nullable=True,
        index=False,
        sa_column_kwargs={"onupdate": utcnow()}
    )


class DeleteResponse(SQLModel):
    deleted: int
