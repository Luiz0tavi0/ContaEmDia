from typing import Optional
from uuid import UUID

from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from .base import TimestampMixin


# from .interfaces import HasUser


class FinancialCategoryBase(SQLModel):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False, index=True, max_length=100)


class FinancialCategory(FinancialCategoryBase, TimestampMixin, table=True):
    __tablename__ = r"financial_categories"

    user_id: UUID = Field(foreign_key="users.id")

    user: Optional['User'] = Relationship(back_populates="categories")

    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='uniqueConstraint_Email_and_User'),
        CheckConstraint('char_length(name) <= 100', name='name_category_max_length')
    )


class FinancialCategoryCreate(FinancialCategoryBase):
    ...


class FinancialCategoryResponse(FinancialCategoryBase):
    ...

