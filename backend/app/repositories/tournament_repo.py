"""
Repositorio de torneos.

Cubre cuatro modelos relacionados jerárquicamente:
- Tournament      : torneo dentro de una temporada.
- TournamentPhase : fase dentro de un torneo.
- PhaseGroup      : grupo dentro de una fase de tipo group_stage.
- GroupTeam       : asignación de un equipo a un grupo.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tournament import GroupTeam, PhaseGroup, Tournament, TournamentPhase
from app.repositories import base


# ─── Tournament ───────────────────────────────────────────────────────────────


async def get_tournament_by_id(session: AsyncSession, tournament_id: UUID) -> Tournament | None:
    return await base.get_by_id(session, Tournament, tournament_id)


async def get_tournaments(
    session: AsyncSession,
    *,
    season_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Tournament]:
    """Lista torneos ordenados por temporada y orden dentro de ella."""
    query = select(Tournament).order_by(Tournament.season_id, Tournament.order)
    if season_id:
        query = query.where(Tournament.season_id == season_id)
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create_tournament(session: AsyncSession, data: dict) -> Tournament:
    return await base.create(session, Tournament, data)


async def update_tournament(session: AsyncSession, tournament: Tournament, data: dict) -> Tournament:
    return await base.update(session, tournament, data)


async def delete_tournament(session: AsyncSession, tournament: Tournament) -> None:
    await base.delete(session, tournament)


# ─── TournamentPhase ──────────────────────────────────────────────────────────


async def get_phase_by_id(session: AsyncSession, phase_id: UUID) -> TournamentPhase | None:
    return await base.get_by_id(session, TournamentPhase, phase_id)


async def get_phases(session: AsyncSession, tournament_id: UUID) -> list[TournamentPhase]:
    """Lista las fases de un torneo ordenadas por su campo order."""
    result = await session.execute(
        select(TournamentPhase)
        .where(TournamentPhase.tournament_id == tournament_id)
        .order_by(TournamentPhase.order)
    )
    return list(result.scalars().all())


async def create_phase(session: AsyncSession, data: dict) -> TournamentPhase:
    return await base.create(session, TournamentPhase, data)


async def update_phase(session: AsyncSession, phase: TournamentPhase, data: dict) -> TournamentPhase:
    return await base.update(session, phase, data)


async def delete_phase(session: AsyncSession, phase: TournamentPhase) -> None:
    await base.delete(session, phase)


# ─── PhaseGroup ───────────────────────────────────────────────────────────────


async def get_group_by_id(session: AsyncSession, group_id: UUID) -> PhaseGroup | None:
    return await base.get_by_id(session, PhaseGroup, group_id)


async def get_groups(session: AsyncSession, phase_id: UUID) -> list[PhaseGroup]:
    """Lista los grupos de una fase ordenados por nombre."""
    result = await session.execute(
        select(PhaseGroup)
        .where(PhaseGroup.phase_id == phase_id)
        .order_by(PhaseGroup.name)
    )
    return list(result.scalars().all())


async def create_group(session: AsyncSession, data: dict) -> PhaseGroup:
    return await base.create(session, PhaseGroup, data)


async def update_group(session: AsyncSession, group: PhaseGroup, data: dict) -> PhaseGroup:
    return await base.update(session, group, data)


async def delete_group(session: AsyncSession, group: PhaseGroup) -> None:
    await base.delete(session, group)


# ─── GroupTeam ────────────────────────────────────────────────────────────────


async def get_group_team_by_id(session: AsyncSession, group_team_id: UUID) -> GroupTeam | None:
    return await base.get_by_id(session, GroupTeam, group_team_id)


async def get_group_teams(session: AsyncSession, group_id: UUID) -> list[GroupTeam]:
    """Lista los equipos asignados a un grupo."""
    result = await session.execute(
        select(GroupTeam).where(GroupTeam.group_id == group_id)
    )
    return list(result.scalars().all())


async def get_group_team(
    session: AsyncSession, group_id: UUID, team_id: UUID
) -> GroupTeam | None:
    """Busca una asignación concreta equipo-grupo. Devuelve None si no existe."""
    result = await session.execute(
        select(GroupTeam).where(
            GroupTeam.group_id == group_id,
            GroupTeam.team_id == team_id,
        )
    )
    return result.scalar_one_or_none()


async def add_team_to_group(session: AsyncSession, data: dict) -> GroupTeam:
    """Asigna un equipo a un grupo."""
    return await base.create(session, GroupTeam, data)


async def remove_team_from_group(session: AsyncSession, group_team: GroupTeam) -> None:
    """Elimina la asignación de un equipo a un grupo."""
    await base.delete(session, group_team)
