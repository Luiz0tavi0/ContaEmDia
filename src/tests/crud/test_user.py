# Filename: test_user.py
import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7

from src.crud.user import UserCRUD
from src.models.user import UserCreate, UserUpdate
from src.tests.conftest_utils import make_random_user


@pytest.mark.asyncio
class TestUserCrud:

    async def test_create_user(self, session: AsyncSession):
        data = await make_random_user(61)
        user = UserCreate(**data)
        created_user = await UserCRUD.create(session, user)

        assert created_user.id is not None
        assert created_user.email == user.email
        assert created_user.created_at is not None

        assert created_user.updated_at is None

    async def test_create_duplicate_user(self, session: AsyncSession):
        data = await make_random_user(60)
        user = UserCreate(**data)
        await UserCRUD.create(session, user)
        try:
            await UserCRUD.create(session, user)
        except HTTPException as e:
            assert e.status_code == 409
            assert e.detail == "User already exists"

    async def test_get_user(self, session: AsyncSession):
        data = await make_random_user(61)
        user = UserCreate(**data)
        created_user = await UserCRUD.create(session, user)
        retrieved_user = await UserCRUD.get_by_id(session, created_user.id)
        assert retrieved_user == created_user

    async def test_get_nonexistent_user(self, session: AsyncSession):
        retrieved_user = await UserCRUD.get_by_id(session, uuid7())
        assert retrieved_user is None

    async def test_get_user_by_email(self, session: AsyncSession):
        data = await make_random_user(61)
        user = UserCreate(**data)
        created_user = await UserCRUD.create(session, user)
        retrieved_user = await UserCRUD.get_by_email(session, user.email)
        assert retrieved_user == created_user

    async def test_get_nonexistent_user_by_email(self, session: AsyncSession):
        retrieved_user = await UserCRUD.get_by_email(session, "nonexistent@example.com")
        assert retrieved_user is None

    async def test_update_user_admin(self, session: AsyncSession):
        data = await make_random_user(61)
        user = UserCreate(**data)

        created_user = await UserCRUD.create(session, user)
        new_data = await make_random_user(61)
        new_data.update(admin=True)
        new_data_user = UserUpdate(**new_data)

        updated_user = await UserCRUD.update(session, created_user.id, new_data_user)
        assert updated_user.id == created_user.id
        assert updated_user.email == data['email']
        assert updated_user.admin is True

    async def test_update_nonexistent_user(self, session: AsyncSession):
        data = await make_random_user(61)
        try:
            new_data_user = UserUpdate(**data)
            await UserCRUD.update(session, uuid7(), new_data_user)
        except HTTPException as e:
            assert e.status_code == 404
            assert e.detail == "User not found"

    async def test_delete_user(self, session: AsyncSession):
        random_user_data = await make_random_user(61)
        random_user_create = UserCreate(**random_user_data)

        created_user = await UserCRUD.create(session, random_user_create)
        deleted_count = await UserCRUD.delete_by_id(session, created_user.id)
        assert deleted_count == 1
        retrieved_user = await UserCRUD.get_by_id(session, created_user.id)
        assert retrieved_user is None

    async def test_delete_nonexistent_user(self, session: AsyncSession):
        deleted_count = await UserCRUD.delete_by_id(session, uuid7())
        assert deleted_count == 0
