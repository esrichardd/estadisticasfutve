"""
Repositorio de ciclos de apercibido (suspension cycles).

Los ciclos se generan automáticamente al registrar tarjetas amarillas;
no se crean ni eliminan directamente vía API. Este repositorio expone
lectura y un update acotado para marcar la suspensión como cumplida.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.suspension import SuspensionCycle
from app.repositories import base


async def get_by_id(session: AsyncSession, cycle_id: UUID) -> SuspensionCycle | None:
    return await base.get_by_id(session, SuspensionCycle, cycle_id)


async def get_all(
    session: AsyncSession,
    *,
    player_id: UUID | None = None,
    is_suspended: bool | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[SuspensionCycle]:
    """
    Lista ciclos de apercibido. Acepta filtro por jugador y/o estado de suspensión,
    ordenados por jugador y número de ciclo.
    """
    query = select(SuspensionCycle).order_by(
        SuspensionCycle.player_id,
        SuspensionCycle.cycle_number,
    )
    if player_id:
        query = query.where(SuspensionCycle.player_id == player_id)
    if is_suspended is not None:
        query = query.where(SuspensionCycle.is_suspended.is_(is_suspended))
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())


async def update(
    session: AsyncSession, cycle: SuspensionCycle, data: dict
) -> SuspensionCycle:
    """Actualiza un ciclo. En la práctica solo se usa para marcar suspension_served."""
    return await base.update(session, cycle, data)
