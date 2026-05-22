"""
Repositorio de equipos.

Contiene las operaciones estándar via base.py más queries específicas
del dominio de equipos (buscar por nombre, filtrar activos, etc.).
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team import Team
from app.repositories import base


async def get_by_id(session: AsyncSession, team_id: UUID) -> Team | None:
    return await base.get_by_id(session, Team, team_id)


async def get_all(
    session: AsyncSession,
    *,
    only_active: bool = False,
    limit: int = 100,
    offset: int = 0,
) -> list[Team]:
    """Lista equipos. Si only_active=True, excluye los archivados."""
    query = select(Team).order_by(Team.name)
    if only_active:
        query = query.where(Team.is_active.is_(True))
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create(session: AsyncSession, data: dict) -> Team:
    return await base.create(session, Team, data)


async def update(session: AsyncSession, team: Team, data: dict) -> Team:
    return await base.update(session, team, data)


async def delete(session: AsyncSession, team: Team) -> None:
    await base.delete(session, team)
