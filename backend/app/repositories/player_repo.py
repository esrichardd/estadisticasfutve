"""
Repositorio de jugadores.

Contiene las operaciones estándar via base.py más queries específicas
del dominio de jugadores (filtrar por posición, buscar por nombre, etc.).
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.player import Player
from app.repositories import base


async def get_by_id(session: AsyncSession, player_id: UUID) -> Player | None:
    return await base.get_by_id(session, Player, player_id)


async def get_all(
    session: AsyncSession,
    *,
    position: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Player]:
    """Lista jugadores. Si position se provee, filtra por esa posición."""
    query = select(Player).order_by(Player.name)
    if position:
        query = query.where(Player.position == position)
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create(session: AsyncSession, data: dict) -> Player:
    return await base.create(session, Player, data)


async def update(session: AsyncSession, player: Player, data: dict) -> Player:
    return await base.update(session, player, data)


async def delete(session: AsyncSession, player: Player) -> None:
    await base.delete(session, player)
