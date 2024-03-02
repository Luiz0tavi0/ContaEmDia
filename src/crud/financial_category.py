from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete, select

from src.models.financial_category import FinancialCategory


class UserCRUD:
    @staticmethod
    async def create(session: AsyncSession, user: UserCreate) -> User:
        db_user = User(**user.dict())
        try:
            session.add(db_user)
            await session.commit()
            return db_user
        except Exception as err:
            await session.rollback()
            raise HTTPException(
                status_code=409,
                detail="User already exists",
            )

    @staticmethod
    async def get_by_id(session: AsyncSession, user_id: UUID) -> User:
        query = select(User).where(User.id == user_id)
        response = await session.execute(query)
        return response.scalar_one_or_none()


async def make_financial_category(session: AsyncSession, fin_category: FinancialCategory) -> FinancialCategory:
    db_fin_category = FinancialCategory(**fin_category.model_dump(exclude_unset=True))
    try:
        session.add(db_fin_category)
        await session.commit()
        await session.refresh(db_fin_category)
        return db_fin_category
    except IntegrityError as err:
        print(err)
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Financial Category already exists",
        )
