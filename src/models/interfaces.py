from sqlmodel import Field, SQLModel
from typing import TYPE_CHECKING


class HasUser:
    if TYPE_CHECKING:
        from .user import User
    user: "User"


class HasFinCategory:
    if TYPE_CHECKING:
        from .financial_category import FinancialCategory

    financial_category: "FinancialCategory"
