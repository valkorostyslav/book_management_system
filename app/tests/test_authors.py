import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import DATABASE_TEST_URL
from app.core.db import AsyncSession, Base, engine

Base = declarative_base()
engine = create_async_engine(DATABASE_TEST_URL, echo=True)
TestingSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def test_db():
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def register_user_and_get_token(test_db: AsyncSession):
    user_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
    }
    response = await AsyncClient().post(
        "http://localhost:8000/user/register", json=user_data
    )
    assert response.status_code == 201

    login_data = {"email": "testuser@example.com", "password": "password123"}
    response = await AsyncClient().post("/auth/jwt/create", json=login_data)
    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_author(register_user_and_get_token):
    token = await register_user_and_get_token
    author_data = {"name": "Test Author", "biography": "Biography of Test Author"}
    response = await AsyncClient().post(
        "http://localhost:8000/author/",
        json=author_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Author"
    assert response.json()["biography"] == "Biography of Test Author"


@pytest.mark.asyncio
async def test_get_all_authors(register_user_and_get_token):
    token = await register_user_and_get_token
    response = await AsyncClient().get(
        "http://localhost:8000/author/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_author_by_id(register_user_and_get_token):
    token = await register_user_and_get_token
    author_data = {"name": "Test Author", "biography": "Biography of Test Author"}
    response = await AsyncClient().post(
        "http://localhost:8000/author/",
        json=author_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    author_id = response.json()["id"]

    response = await AsyncClient().get(
        f"http://localhost:8000/author/{author_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == author_id


@pytest.mark.asyncio
async def test_update_author(register_user_and_get_token):
    token = await register_user_and_get_token
    author_data = {"name": "Test Author", "biography": "Biography of Test Author"}
    response = await AsyncClient().post(
        "http://localhost:8000/author/",
        json=author_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    author_id = response.json()["id"]

    update_data = {"name": "Updated Author", "biography": "Updated Biography"}
    response = await AsyncClient().put(
        f"http://localhost:8000/author/{author_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Author"
    assert response.json()["biography"] == "Updated Biography"


@pytest.mark.asyncio
async def test_delete_author(register_user_and_get_token):
    token = await register_user_and_get_token
    author_data = {"name": "Test Author", "biography": "Biography of Test Author"}
    response = await AsyncClient().post(
        "http://localhost:8000/author/",
        json=author_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    author_id = response.json()["id"]

    response = await AsyncClient().delete(
        f"http://localhost:8000/author/{author_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

    response = await AsyncClient().get(
        f"http://localhost:8000/author/{author_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
