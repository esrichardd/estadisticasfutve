"""
Repositorio de partidos.

Cubre cuatro modelos relacionados jerárquicamente:
- Round         : jornada dentro de una fase (y opcionalmente de un grupo).
- Match         : partido entre dos equipos dentro de una jornada.
- MatchOfficial : árbitros asignados a un partido.
- MatchEvent    : eventos ocurridos en un partido (goles, tarjetas, etc.).
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.match import Match, MatchEvent, MatchOfficial, Round
from app.repositories import base


# ─── Round ────────────────────────────────────────────────────────────────────


async def get_round_by_id(session: AsyncSession, round_id: UUID) -> Round | None:
    return await base.get_by_id(session, Round, round_id)


async def get_rounds(
    session: AsyncSession,
    *,
    phase_id: UUID | None = None,
    group_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Round]:
    """Lista jornadas. Acepta filtro por fase y/o grupo, ordenadas por número."""
    query = select(Round).order_by(Round.number)
    if phase_id:
        query = query.where(Round.phase_id == phase_id)
    if group_id:
        query = query.where(Round.group_id == group_id)
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create_round(session: AsyncSession, data: dict) -> Round:
    return await base.create(session, Round, data)


async def update_round(session: AsyncSession, round_: Round, data: dict) -> Round:
    return await base.update(session, round_, data)


async def delete_round(session: AsyncSession, round_: Round) -> None:
    await base.delete(session, round_)


# ─── Match ────────────────────────────────────────────────────────────────────


async def get_match_by_id(session: AsyncSession, match_id: UUID) -> Match | None:
    return await base.get_by_id(session, Match, match_id)


async def get_matches(
    session: AsyncSession,
    *,
    round_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Match]:
    """Lista partidos. Acepta filtro por jornada, ordenados por fecha programada."""
    query = select(Match).order_by(Match.scheduled_datetime)
    if round_id:
        query = query.where(Match.round_id == round_id)
    result = await session.execute(query.offset(offset).limit(limit))
    return list(result.scalars().all())


async def create_match(session: AsyncSession, data: dict) -> Match:
    return await base.create(session, Match, data)


async def update_match(session: AsyncSession, match: Match, data: dict) -> Match:
    return await base.update(session, match, data)


async def delete_match(session: AsyncSession, match: Match) -> None:
    await base.delete(session, match)


# ─── MatchOfficial ────────────────────────────────────────────────────────────


async def get_official_by_id(session: AsyncSession, official_id: UUID) -> MatchOfficial | None:
    return await base.get_by_id(session, MatchOfficial, official_id)


async def get_officials(session: AsyncSession, match_id: UUID) -> list[MatchOfficial]:
    """Lista los árbitros asignados a un partido."""
    result = await session.execute(
        select(MatchOfficial).where(MatchOfficial.match_id == match_id)
    )
    return list(result.scalars().all())


async def get_official_by_referee(
    session: AsyncSession, match_id: UUID, referee_id: UUID
) -> MatchOfficial | None:
    """Busca si un árbitro concreto ya está asignado al partido."""
    result = await session.execute(
        select(MatchOfficial).where(
            MatchOfficial.match_id == match_id,
            MatchOfficial.referee_id == referee_id,
        )
    )
    return result.scalar_one_or_none()


async def add_official(session: AsyncSession, data: dict) -> MatchOfficial:
    """Asigna un árbitro a un partido."""
    return await base.create(session, MatchOfficial, data)


async def remove_official(session: AsyncSession, official: MatchOfficial) -> None:
    """Elimina la designación de un árbitro en un partido."""
    await base.delete(session, official)


# ─── MatchEvent ───────────────────────────────────────────────────────────────


async def get_event_by_id(session: AsyncSession, event_id: UUID) -> MatchEvent | None:
    return await base.get_by_id(session, MatchEvent, event_id)


async def get_events(session: AsyncSession, match_id: UUID) -> list[MatchEvent]:
    """Lista los eventos de un partido ordenados por minuto."""
    result = await session.execute(
        select(MatchEvent)
        .where(MatchEvent.match_id == match_id)
        .order_by(MatchEvent.minute, MatchEvent.added_time)
    )
    return list(result.scalars().all())


async def create_event(session: AsyncSession, data: dict) -> MatchEvent:
    return await base.create(session, MatchEvent, data)


async def update_event(session: AsyncSession, event: MatchEvent, data: dict) -> MatchEvent:
    return await base.update(session, event, data)


async def delete_event(session: AsyncSession, event: MatchEvent) -> None:
    await base.delete(session, event)
