import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/mydatabase",
)
DATABASE_TEST_URL = os.getenv(
    "DATABASE_TEST_URL", "postgresql+asyncpg://user:password@localhost:5432/mydatabase"
)
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
