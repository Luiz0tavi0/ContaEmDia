from typing import Dict, Callable
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import generic_fn_descriptor
from sqlalchemy.util.langhelpers import _memoized_property, _T_co
from sqlmodel import select

from src.models.user import UserCreate, User, UserUpdate


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

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User:
        query = select(User).where(User.email == email)
        response = await session.execute(query)
        return response.scalar_one_or_none()

    @staticmethod
    async def update(session: AsyncSession, user_id: UUID, user: UserUpdate) -> User:
        db_user = await UserCRUD.get_by_id(session, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        for k, v in user.dict(exclude_unset=True).items():
            setattr(db_user, k, v)

        try:
            await session.commit()
            await session.refresh(db_user)
            return db_user
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Updated user collides with other users",
            )

    @staticmethod
    async def delete_by_id(session: AsyncSession, user_id: UUID) -> Callable[[], int]:
        query = delete(User).where(bool(user_id == User.id))
        response = await session.execute(query)
        await session.commit()
        rows_affected = response.rowcount
        if rows_affected != 1:
            raise HTTPException(status_code=404, detail="User not found")
        return rows_affected

# async def create_user( AsyncSession, user: UserCreate) -> User:
#     db_user = User(**user.dict())
#     try:
#         session.add(db_user)
#         await session.commit()
#         await session.refresh(db_user)
#         return db_user
#     except IntegrityError as err:
#         print(err)
#         await session.rollback()
#         raise HTTPException(
#             status_code=409,
#             detail="User already exists",
#         )
# 
# async def get_user( AsyncSession, user_id: UUID) -> User:
#     query = select(User).where(User.id == user_id)
#     response = await session.execute(query)
#     return response.scalar_one_or_none()
# 
# async def get_user_by_email( AsyncSession, email: str) -> User:
#     query = select(User).where(User.email == email)
#     response = await session.execute(query)
#     return response.scalar_one_or_none()
# 
# async def update_user( AsyncSession, user_id: UUID, user: UserUpdate) -> User:
#     db_user = await get_user(session, id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
# 
#     for k, v in user.dict(exclude_unset=True).items():
#         setattr(db_user, k, v)
# 
#     try:
#         await session.commit()
#         await session.refresh(db_user)
#         return db_user
#     except IntegrityError:
#         session.rollback()
#         raise HTTPException(
#             status_code=409,
#             detail="Updated user collides with other users",
#         )
# 
# async def delete_user( AsyncSession, user_id: UUID) -> int:
#     query = delete(User).where(User.id == user_id)
#     response = await session.execute(query)
#     await session.commit()
#     return await response.rowcount
