import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

# DATABASE_URL viene de la variable de entorno definida en docker-compose / .env
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:secret123@postgres:5432/appdb",
)

# Engine async (asyncpg como driver)
engine = create_async_engine(DATABASE_URL, echo=True)

# Factory de sesiones async
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos SQLAlchemy."""
    pass


async def get_db() -> AsyncSession:
    """Dependency de FastAPI: provee una sesión async y la cierra al terminar."""
    async with AsyncSessionLocal() as session:
        yield session
