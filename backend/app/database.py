from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# Engine async — echo solo en desarrollo para ver las queries en los logs
engine = create_async_engine(
    settings.database_url,
    echo=settings.environment == "development",
)

# Fábrica de sesiones async
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos SQLAlchemy."""
    pass


async def get_db():
    """
    Dependency de FastAPI: abre una sesión async y la cierra al terminar,
    sin importar si hubo error o no.

    Uso en un router:
        async def mi_endpoint(db: AsyncSession = Depends(get_db)): ...
    """
    async with AsyncSessionLocal() as session:
        yield session
