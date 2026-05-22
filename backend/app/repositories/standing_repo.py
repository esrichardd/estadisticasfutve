"""
Repositorio de posiciones (standings).

Las posiciones se recalculan automáticamente al finalizar cada partido;
no se crean ni modifican directamente vía API. Este repositorio solo expone
operaciones de lectura.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.standing import Standing
from app.repositories import base


async def get_by_id(session: AsyncSession, standing_id: UUID) -> Standing | None:
    return await base.get_by_id(session, Standing, standing_id)


async def get_all(
    session: AsyncSession,
    *,
    phase_id: UUID | None = None,
    group_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Standing]:
    """
    Lista posiciones ordenadas por puntos DESC, diferencia de goles DESC.
    Acepta filtro por fase y/o grupo.
    """
    query = select(Standing).order_by(
        Standing.points.desc(),
        Standing.goal_difference.desc(),
        Standing.goals_for.desc(),
    )
    if phase_id:
        query = query.where(Standing.phase_id == phase_id)
    if group_id:
        query = query.where(Standing.group_id == group_id)
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())
