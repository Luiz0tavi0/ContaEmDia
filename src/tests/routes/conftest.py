import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient


class BaseTestRouter:
    @pytest_asyncio.fixture(scope="function")
    async def client(self, session):
        app = FastAPI()
        app.include_router(self.router)
        app.dependency_overrides[session] = lambda: session
        async with AsyncClient(app=app, base_url="http://test") as c:
            yield c
