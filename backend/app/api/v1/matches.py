from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import match_repo
from app.schemas.match import (
    MatchCreate,
    MatchEventCreate,
    MatchEventResponse,
    MatchEventUpdate,
    MatchOfficialCreate,
    MatchOfficialResponse,
    MatchResponse,
    MatchUpdate,
    RoundCreate,
    RoundResponse,
    RoundUpdate,
)

router = APIRouter(tags=["matches"])


# ─── Round ────────────────────────────────────────────────────────────────────


@router.get("/rounds/", response_model=list[RoundResponse])
async def list_rounds(
    phase_id: UUID | None = None,
    group_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Lista jornadas. Acepta filtro por fase y/o grupo, y paginación."""
    return await match_repo.get_rounds(db, phase_id=phase_id, group_id=group_id, limit=limit, offset=offset)


@router.get("/rounds/{round_id}", response_model=RoundResponse)
async def get_round(round_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve una jornada por su ID. 404 si no existe."""
    round_ = await match_repo.get_round_by_id(db, round_id)
    if not round_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada no encontrada")
    return round_


@router.post("/rounds/", response_model=RoundResponse, status_code=status.HTTP_201_CREATED)
async def create_round(data: RoundCreate, db: AsyncSession = Depends(get_db)):
    """Crea una nueva jornada."""
    return await match_repo.create_round(db, data.model_dump())


@router.patch("/rounds/{round_id}", response_model=RoundResponse)
async def update_round(round_id: UUID, data: RoundUpdate, db: AsyncSession = Depends(get_db)):
    """Actualiza solo los campos enviados en una jornada (PATCH semántico)."""
    round_ = await match_repo.get_round_by_id(db, round_id)
    if not round_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada no encontrada")
    return await match_repo.update_round(db, round_, data.model_dump(exclude_none=True))


@router.delete("/rounds/{round_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_round(round_id: UUID, db: AsyncSession = Depends(get_db)):
    """Elimina una jornada. 404 si no existe."""
    round_ = await match_repo.get_round_by_id(db, round_id)
    if not round_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada no encontrada")
    await match_repo.delete_round(db, round_)


# ─── Match ────────────────────────────────────────────────────────────────────


@router.get("/rounds/{round_id}/matches", response_model=list[MatchResponse])
async def list_matches_by_round(round_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lista los partidos de una jornada."""
    round_ = await match_repo.get_round_by_id(db, round_id)
    if not round_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jornada no encontrada")
    return await match_repo.get_matches(db, round_id=round_id)


@router.get("/matches/{match_id}", response_model=MatchResponse)
async def get_match(match_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve un partido por su ID. 404 si no existe."""
    match = await match_repo.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    return match


@router.post("/matches/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def create_match(data: MatchCreate, db: AsyncSession = Depends(get_db)):
    """Crea un nuevo partido."""
    return await match_repo.create_match(db, data.model_dump())


@router.patch("/matches/{match_id}", response_model=MatchResponse)
async def update_match(match_id: UUID, data: MatchUpdate, db: AsyncSession = Depends(get_db)):
    """Actualiza solo los campos enviados en un partido (PATCH semántico)."""
    match = await match_repo.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    return await match_repo.update_match(db, match, data.model_dump(exclude_none=True))


@router.delete("/matches/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(match_id: UUID, db: AsyncSession = Depends(get_db)):
    """Elimina un partido. 404 si no existe."""
    match = await match_repo.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    await match_repo.delete_match(db, match)


# ─── MatchOfficial ────────────────────────────────────────────────────────────


@router.get("/matches/{match_id}/officials", response_model=list[MatchOfficialResponse])
async def list_officials(match_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lista los árbitros asignados a un partido."""
    match = await match_repo.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    return await match_repo.get_officials(db, match_id)


@router.post(
    "/matches/{match_id}/officials",
    response_model=MatchOfficialResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_official(
    match_id: UUID, data: MatchOfficialCreate, db: AsyncSession = Depends(get_db)
):
    """Asigna un árbitro a un partido. 409 si el árbitro ya está asignado."""
    match = await match_repo.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    existing = await match_repo.get_official_by_referee(db, match_id, data.referee_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El árbitro ya está asignado a este partido",
        )
    payload = data.model_dump()
    payload["match_id"] = match_id
    return await match_repo.add_official(db, payload)


@router.delete("/matches/{match_id}/officials/{official_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_official(
    match_id: UUID, official_id: UUID, db: AsyncSession = Depends(get_db)
):
    """Elimina la designación de un árbitro en un partido. 404 si no existe."""
    official = await match_repo.get_official_by_id(db, official_id)
    if not official or official.match_id != match_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Designación de árbitro no encontrada",
        )
    await match_repo.remove_official(db, official)


# ─── MatchEvent ───────────────────────────────────────────────────────────────


@router.get("/matches/{match_id}/events", response_model=list[MatchEventResponse])
async def list_events(match_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lista los eventos de un partido ordenados por minuto."""
    match = await match_repo.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    return await match_repo.get_events(db, match_id)


@router.post(
    "/matches/{match_id}/events",
    response_model=MatchEventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    match_id: UUID, data: MatchEventCreate, db: AsyncSession = Depends(get_db)
):
    """Registra un nuevo evento en un partido."""
    match = await match_repo.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")
    payload = data.model_dump()
    payload["match_id"] = match_id
    return await match_repo.create_event(db, payload)


@router.patch("/matches/{match_id}/events/{event_id}", response_model=MatchEventResponse)
async def update_event(
    match_id: UUID, event_id: UUID, data: MatchEventUpdate, db: AsyncSession = Depends(get_db)
):
    """Actualiza solo los campos enviados en un evento (PATCH semántico)."""
    event = await match_repo.get_event_by_id(db, event_id)
    if not event or event.match_id != match_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    return await match_repo.update_event(db, event, data.model_dump(exclude_none=True))


@router.delete("/matches/{match_id}/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    match_id: UUID, event_id: UUID, db: AsyncSession = Depends(get_db)
):
    """Elimina un evento de un partido. 404 si no existe."""
    event = await match_repo.get_event_by_id(db, event_id)
    if not event or event.match_id != match_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    await match_repo.delete_event(db, event)
