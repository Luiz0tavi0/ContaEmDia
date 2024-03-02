import pytest

from src.api.routes.v1.c import router as user_router
from src.crud.user import *
from src.models.user import UserCreate
from src.tests.conftest_utils import make_random_user
from src.tests.routes.conftest import BaseTestRouter


@pytest.mark.asyncio
class TestUserRouter(BaseTestRouter):
    router = user_router

    async def test_create_user(self, client):
        data = await make_random_user(password_length=61)
        response = await client.post("/users/", json=data)
        assert response.status_code == 201
        assert response.json()["email"] == data["email"]

    async def test_get_user(self, session: AsyncSession, client):
        data = await make_random_user(password_length=61)
        user = await UserCRUD.create(session, UserCreate(**data))
        response = await client.get(f"/users/{user.id}")
        assert response.status_code == 200
        assert response.json()["email"] == user.email

    async def test_update_user(self, session: AsyncSession, client):
        data = await make_random_user(password_length=61)

        user = await UserCRUD.create(session, UserCreate(**data))
        response = await client.patch(
            f"/users/{user.id}", json=dict(email="test1@example.com")
        )
        assert response.status_code == 200
        assert response.json()["email"] == user.email

        user_updated = await UserCRUD.get_by_id(session, user_id=user.id)
        assert user_updated.email == "test1@example.com"

    async def test_delete_user(self, session: AsyncSession, client):
        # Arrange
        data = await make_random_user(password_length=61)
        user = await UserCRUD.create(session, UserCreate(**data))
        # Act
        response = await client.delete(f"/users/{user.id}")

        # Assert
        assert response.status_code == 200
        assert response.json() == dict(deleted=1)

        user_deleted = await UserCRUD.get_by_id(session, user_id=user.id)
        assert user_deleted is None
