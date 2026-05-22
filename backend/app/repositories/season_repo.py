"""
Repositorio de temporadas.

Cubre dos modelos:
- Season: operaciones estándar + filtro por liga.
- SeasonTeam: gestión de equipos participantes en una temporada.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.season import Season, SeasonTeam
from app.repositories import base


# ─── Season ───────────────────────────────────────────────────────────────────


async def get_by_id(session: AsyncSession, season_id: UUID) -> Season | None:
    return await base.get_by_id(session, Season, season_id)


async def get_all(
    session: AsyncSession,
    *,
    league_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Season]:
    """Lista temporadas. Si league_id se provee, filtra por esa liga."""
    query = select(Season).order_by(Season.start_date.desc())
    if league_id:
        query = query.where(Season.league_id == league_id)
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create(session: AsyncSession, data: dict) -> Season:
    return await base.create(session, Season, data)


async def update(session: AsyncSession, season: Season, data: dict) -> Season:
    return await base.update(session, season, data)


async def delete(session: AsyncSession, season: Season) -> None:
    await base.delete(session, season)


# ─── SeasonTeam ───────────────────────────────────────────────────────────────


async def get_teams(session: AsyncSession, season_id: UUID) -> list[SeasonTeam]:
    """Devuelve los registros SeasonTeam de una temporada."""
    result = await session.execute(
        select(SeasonTeam).where(SeasonTeam.season_id == season_id)
    )
    return list(result.scalars().all())


async def get_season_team(
    session: AsyncSession, season_id: UUID, team_id: UUID
) -> SeasonTeam | None:
    """Busca un SeasonTeam concreto. Devuelve None si no existe."""
    result = await session.execute(
        select(SeasonTeam).where(
            SeasonTeam.season_id == season_id,
            SeasonTeam.team_id == team_id,
        )
    )
    return result.scalar_one_or_none()


async def add_team(session: AsyncSession, season_id: UUID, team_id: UUID) -> SeasonTeam:
    """Inscribe un equipo en una temporada."""
    return await base.create(session, SeasonTeam, {"season_id": season_id, "team_id": team_id})


async def remove_team(session: AsyncSession, season_team: SeasonTeam) -> None:
    """Elimina la inscripción de un equipo en una temporada."""
    await base.delete(session, season_team)
