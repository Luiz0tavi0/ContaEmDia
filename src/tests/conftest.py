# Filename: conftest.py
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="class")
async def engine(event_loop):
    engine = create_async_engine(settings.ASYNC_POSTGRES_URI, echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope='class')
async def session(engine):
    SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False,
                                autoflush=False)
    async with SessionLocal() as session:
        yield session
    await session.close()
