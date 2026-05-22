"""
Repositorio de ligas.

Contiene las operaciones estándar via base.py más queries específicas
del dominio de ligas (filtrar por activas, por país, etc.).
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.league import League
from app.repositories import base


async def get_by_id(session: AsyncSession, league_id: UUID) -> League | None:
    return await base.get_by_id(session, League, league_id)


async def get_all(
    session: AsyncSession,
    *,
    only_active: bool = False,
    country: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[League]:
    """Lista ligas. Acepta filtro por activas y por país."""
    query = select(League).order_by(League.name)
    if only_active:
        query = query.where(League.is_active.is_(True))
    if country:
        query = query.where(League.country == country)
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create(session: AsyncSession, data: dict) -> League:
    return await base.create(session, League, data)


async def update(session: AsyncSession, league: League, data: dict) -> League:
    return await base.update(session, league, data)


async def delete(session: AsyncSession, league: League) -> None:
    await base.delete(session, league)
