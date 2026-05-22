"""
Repositorio de árbitros.

Contiene las operaciones estándar via base.py más queries específicas
del dominio de árbitros (filtrar por activos, por nacionalidad, etc.).
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.referee import Referee
from app.repositories import base


async def get_by_id(session: AsyncSession, referee_id: UUID) -> Referee | None:
    return await base.get_by_id(session, Referee, referee_id)


async def get_all(
    session: AsyncSession,
    *,
    only_active: bool = False,
    nationality: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Referee]:
    """Lista árbitros. Acepta filtro por activos y por nacionalidad."""
    query = select(Referee).order_by(Referee.name)
    if only_active:
        query = query.where(Referee.is_active.is_(True))
    if nationality:
        query = query.where(Referee.nationality == nationality)
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create(session: AsyncSession, data: dict) -> Referee:
    return await base.create(session, Referee, data)


async def update(session: AsyncSession, referee: Referee, data: dict) -> Referee:
    return await base.update(session, referee, data)


async def delete(session: AsyncSession, referee: Referee) -> None:
    await base.delete(session, referee)
