from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import tournament_repo
from app.schemas.tournament import (
    GroupTeamCreate,
    GroupTeamResponse,
    PhaseGroupCreate,
    PhaseGroupResponse,
    PhaseGroupUpdate,
    TournamentCreate,
    TournamentPhaseCreate,
    TournamentPhaseResponse,
    TournamentPhaseUpdate,
    TournamentResponse,
    TournamentUpdate,
)

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


# ─── Tournament ───────────────────────────────────────────────────────────────


@router.get("/", response_model=list[TournamentResponse])
async def list_tournaments(
    season_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Lista todos los torneos. Acepta filtro por temporada y paginación."""
    return await tournament_repo.get_tournaments(db, season_id=season_id, limit=limit, offset=offset)


@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(tournament_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve un torneo por su ID. 404 si no existe."""
    tournament = await tournament_repo.get_tournament_by_id(db, tournament_id)
    if not tournament:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Torneo no encontrado")
    return tournament


@router.post("/", response_model=TournamentResponse, status_code=status.HTTP_201_CREATED)
async def create_tournament(data: TournamentCreate, db: AsyncSession = Depends(get_db)):
    """Crea un nuevo torneo."""
    return await tournament_repo.create_tournament(db, data.model_dump())


@router.patch("/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(tournament_id: UUID, data: TournamentUpdate, db: AsyncSession = Depends(get_db)):
    """Actualiza solo los campos enviados (PATCH semántico)."""
    tournament = await tournament_repo.get_tournament_by_id(db, tournament_id)
    if not tournament:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Torneo no encontrado")
    return await tournament_repo.update_tournament(db, tournament, data.model_dump(exclude_none=True))


@router.delete("/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tournament(tournament_id: UUID, db: AsyncSession = Depends(get_db)):
    """Elimina un torneo. 404 si no existe."""
    tournament = await tournament_repo.get_tournament_by_id(db, tournament_id)
    if not tournament:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Torneo no encontrado")
    await tournament_repo.delete_tournament(db, tournament)


# ─── TournamentPhase ──────────────────────────────────────────────────────────


@router.get("/{tournament_id}/phases", response_model=list[TournamentPhaseResponse])
async def list_phases(tournament_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lista las fases de un torneo ordenadas por su campo order."""
    tournament = await tournament_repo.get_tournament_by_id(db, tournament_id)
    if not tournament:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Torneo no encontrado")
    return await tournament_repo.get_phases(db, tournament_id)


@router.post(
    "/{tournament_id}/phases",
    response_model=TournamentPhaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_phase(
    tournament_id: UUID, data: TournamentPhaseCreate, db: AsyncSession = Depends(get_db)
):
    """Crea una nueva fase dentro del torneo indicado."""
    tournament = await tournament_repo.get_tournament_by_id(db, tournament_id)
    if not tournament:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Torneo no encontrado")
    payload = data.model_dump()
    payload["tournament_id"] = tournament_id
    return await tournament_repo.create_phase(db, payload)


@router.patch("/phases/{phase_id}", response_model=TournamentPhaseResponse)
async def update_phase(
    phase_id: UUID, data: TournamentPhaseUpdate, db: AsyncSession = Depends(get_db)
):
    """Actualiza solo los campos enviados en una fase (PATCH semántico)."""
    phase = await tournament_repo.get_phase_by_id(db, phase_id)
    if not phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fase no encontrada")
    return await tournament_repo.update_phase(db, phase, data.model_dump(exclude_none=True))


@router.delete("/phases/{phase_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_phase(phase_id: UUID, db: AsyncSession = Depends(get_db)):
    """Elimina una fase. 404 si no existe."""
    phase = await tournament_repo.get_phase_by_id(db, phase_id)
    if not phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fase no encontrada")
    await tournament_repo.delete_phase(db, phase)


# ─── PhaseGroup ───────────────────────────────────────────────────────────────


@router.get("/phases/{phase_id}/groups", response_model=list[PhaseGroupResponse])
async def list_groups(phase_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lista los grupos de una fase."""
    phase = await tournament_repo.get_phase_by_id(db, phase_id)
    if not phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fase no encontrada")
    return await tournament_repo.get_groups(db, phase_id)


@router.post(
    "/phases/{phase_id}/groups",
    response_model=PhaseGroupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_group(
    phase_id: UUID, data: PhaseGroupCreate, db: AsyncSession = Depends(get_db)
):
    """Crea un nuevo grupo dentro de la fase indicada."""
    phase = await tournament_repo.get_phase_by_id(db, phase_id)
    if not phase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fase no encontrada")
    payload = data.model_dump()
    payload["phase_id"] = phase_id
    return await tournament_repo.create_group(db, payload)


@router.patch("/groups/{group_id}", response_model=PhaseGroupResponse)
async def update_group(
    group_id: UUID, data: PhaseGroupUpdate, db: AsyncSession = Depends(get_db)
):
    """Actualiza solo los campos enviados en un grupo (PATCH semántico)."""
    group = await tournament_repo.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return await tournament_repo.update_group(db, group, data.model_dump(exclude_none=True))


@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: UUID, db: AsyncSession = Depends(get_db)):
    """Elimina un grupo. 404 si no existe."""
    group = await tournament_repo.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    await tournament_repo.delete_group(db, group)


# ─── GroupTeam ────────────────────────────────────────────────────────────────


@router.get("/groups/{group_id}/teams", response_model=list[GroupTeamResponse])
async def list_group_teams(group_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lista los equipos asignados a un grupo."""
    group = await tournament_repo.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    return await tournament_repo.get_group_teams(db, group_id)


@router.post(
    "/groups/{group_id}/teams",
    response_model=GroupTeamResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_team_to_group(
    group_id: UUID, data: GroupTeamCreate, db: AsyncSession = Depends(get_db)
):
    """Asigna un equipo a un grupo. 409 si el equipo ya está en ese grupo."""
    group = await tournament_repo.get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")
    existing = await tournament_repo.get_group_team(db, group_id, data.team_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El equipo ya está asignado a este grupo",
        )
    payload = data.model_dump()
    payload["group_id"] = group_id
    return await tournament_repo.add_team_to_group(db, payload)


@router.delete("/groups/{group_id}/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_team_from_group(
    group_id: UUID, team_id: UUID, db: AsyncSession = Depends(get_db)
):
    """Elimina la asignación de un equipo a un grupo. 404 si no existe."""
    group_team = await tournament_repo.get_group_team(db, group_id, team_id)
    if not group_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El equipo no está asignado a este grupo",
        )
    await tournament_repo.remove_team_from_group(db, group_team)
