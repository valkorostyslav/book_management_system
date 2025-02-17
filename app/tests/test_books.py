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
async def test_create_book(register_user_and_get_token):
    token = await register_user_and_get_token
    response = await AsyncClient().post(
        "http://localhost:8000/book",
        json={"title": "Test Book", "author": "John Doe"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"
    assert response.json()["author"] == "John Doe"


@pytest.mark.asyncio
async def test_get_books(register_user_and_get_token):
    token = await register_user_and_get_token
    response = await AsyncClient().get(
        "http://localhost:8000/book", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_book_by_id(register_user_and_get_token):
    token = await register_user_and_get_token
    book_data = {"title": "Unique Book", "author": "Author Name"}
    response = await AsyncClient().post(
        "http://localhost:8000/book",
        json=book_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    book_id = response.json()["id"]

    response = await AsyncClient().get(
        f"http://localhost:8000/book/{book_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["id"] == book_id
    assert response.json()["title"] == "Unique Book"
    assert response.json()["author"] == "Author Name"


@pytest.mark.asyncio
async def test_update_book(register_user_and_get_token):
    token = await register_user_and_get_token
    book_data = {"title": "Old Title", "author": "Old Author"}
    response = await AsyncClient().post(
        "http://localhost:8000/book",
        json=book_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    book_id = response.json()["id"]

    updated_data = {"title": "New Title", "author": "New Author"}
    response = await AsyncClient().put(
        f"http://localhost:8000/book/{book_id}",
        json=updated_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["author"] == "New Author"


@pytest.mark.asyncio
async def test_delete_book(register_user_and_get_token):
    token = await register_user_and_get_token
    book_data = {"title": "To Delete", "author": "Someone"}
    response = await AsyncClient().post(
        "http://localhost:8000/book",
        json=book_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    book_id = response.json()["id"]

    response = await AsyncClient().delete(
        f"http://localhost:8000/book/{book_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 204

    response = await AsyncClient().get(
        f"http://localhost:8000/book/{book_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
