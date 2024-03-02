from typing import List, Optional, Any
from uuid import UUID

from email_validator import validate_email, EmailNotValidError
from pydantic import field_validator
from pydantic.v1 import validator
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship
from uuid_extensions import uuid7

from .base import TimestampMixin
from .financial_category import FinancialCategory


class UserBase(SQLModel):
    email: str = Field(nullable=False, index=True)
    admin: bool = Field(default_factory=lambda: False)
    email_confirmed: bool = Field(default_factory=lambda: False)
    password: str = Field(nullable=False, min_length=9)


class User(TimestampMixin, UserBase, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid7, primary_key=True, index=True)
    categories: Optional[List["FinancialCategory"]] = Relationship(back_populates="user")

    class Config:
        from_attributes = True

    __table_args__ = (
        UniqueConstraint('email', name='uniqueConstraint_Email_for_User'),
        CheckConstraint('char_length(password) >= 60', name='password_min_length')
    )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id

class UserCreate(UserBase):
    # @validator('email')
    @field_validator('email')
    def email_validate(cls, email: str) -> str:
        try:
            email_info = validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            raise ValueError('Email must be valid.')
        return email_info.normalized


class UserUpdate(SQLModel):
    password: Optional[str] = None
    admin: bool = False

    @validator('email')
    def email_validate(cls, email: str) -> str:
        return UserCreate.email_validate(email)  # Reuse email validation logic from UserCreate


class UserResponse(UserBase, table=False):
    id: UUID
