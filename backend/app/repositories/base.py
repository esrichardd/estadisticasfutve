"""
Funciones genéricas de acceso a datos reutilizables por todos los repositorios.

Uso:
    from app.repositories.base import get_by_id, get_all, create, update, delete
    from app.models.team import Team

    team = await get_by_id(session, Team, team_id)
    teams = await get_all(session, Team)
"""

from typing import Any, Type, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


async def get_by_id(
    session: AsyncSession,
    model: Type[ModelType],
    id: UUID,
) -> ModelType | None:
    """Busca un registro por su PK. Devuelve None si no existe."""
    result = await session.execute(select(model).where(model.id == id))
    return result.scalar_one_or_none()


async def get_all(
    session: AsyncSession,
    model: Type[ModelType],
    *,
    limit: int = 100,
    offset: int = 0,
) -> list[ModelType]:
    """Lista registros con paginación básica."""
    result = await session.execute(
        select(model).order_by(model.id).offset(offset).limit(limit)
    )
    return list(result.scalars().all())


async def create(
    session: AsyncSession,
    model: Type[ModelType],
    data: dict[str, Any],
) -> ModelType:
    """Crea un registro y lo devuelve con los datos del DB (id, timestamps, etc.)."""
    instance = model(**data)
    session.add(instance)
    await session.commit()
    await session.refresh(instance)
    return instance


async def update(
    session: AsyncSession,
    instance: ModelType,
    data: dict[str, Any],
) -> ModelType:
    """
    Actualiza solo los campos incluidos en data (PATCH semántico).
    Recibe la instancia ya cargada, no el ID.
    """
    for field, value in data.items():
        setattr(instance, field, value)
    await session.commit()
    await session.refresh(instance)
    return instance


async def delete(
    session: AsyncSession,
    instance: ModelType,
) -> None:
    """Elimina el registro. Recibe la instancia ya cargada."""
    await session.delete(instance)
    await session.commit()
