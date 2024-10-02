import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_async_session
from src.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async_engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_async_session():
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="module")
async def async_client() -> AsyncClient:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
