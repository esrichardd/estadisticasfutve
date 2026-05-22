from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import season_repo
from app.schemas.season import (
    SeasonCreate,
    SeasonResponse,
    SeasonTeamCreate,
    SeasonTeamResponse,
    SeasonUpdate,
)

router = APIRouter(prefix="/seasons", tags=["seasons"])


# ─── Season ───────────────────────────────────────────────────────────────────


@router.get("/", response_model=list[SeasonResponse])
async def list_seasons(
    league_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Lista todas las temporadas. Acepta filtro por liga y paginación."""
    return await season_repo.get_all(db, league_id=league_id, limit=limit, offset=offset)


@router.get("/{season_id}", response_model=SeasonResponse)
async def get_season(season_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve una temporada por su ID. 404 si no existe."""
    season = await season_repo.get_by_id(db, season_id)
    if not season:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temporada no encontrada")
    return season


@router.post("/", response_model=SeasonResponse, status_code=status.HTTP_201_CREATED)
async def create_season(data: SeasonCreate, db: AsyncSession = Depends(get_db)):
    """Crea una nueva temporada."""
    return await season_repo.create(db, data.model_dump())


@router.patch("/{season_id}", response_model=SeasonResponse)
async def update_season(season_id: UUID, data: SeasonUpdate, db: AsyncSession = Depends(get_db)):
    """Actualiza solo los campos enviados (PATCH semántico)."""
    season = await season_repo.get_by_id(db, season_id)
    if not season:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temporada no encontrada")
    return await season_repo.update(db, season, data.model_dump(exclude_none=True))


# ─── SeasonTeam ───────────────────────────────────────────────────────────────


@router.get("/{season_id}/teams", response_model=list[SeasonTeamResponse])
async def list_season_teams(season_id: UUID, db: AsyncSession = Depends(get_db)):
    """Lista los equipos inscritos en una temporada."""
    season = await season_repo.get_by_id(db, season_id)
    if not season:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temporada no encontrada")
    return await season_repo.get_teams(db, season_id)


@router.post("/{season_id}/teams", response_model=SeasonTeamResponse, status_code=status.HTTP_201_CREATED)
async def add_team_to_season(
    season_id: UUID, data: SeasonTeamCreate, db: AsyncSession = Depends(get_db)
):
    """Inscribe un equipo en una temporada. 409 si ya está inscrito."""
    season = await season_repo.get_by_id(db, season_id)
    if not season:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Temporada no encontrada")
    existing = await season_repo.get_season_team(db, season_id, data.team_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El equipo ya está inscrito en esta temporada")
    return await season_repo.add_team(db, season_id, data.team_id)


@router.delete("/{season_id}/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_team_from_season(
    season_id: UUID, team_id: UUID, db: AsyncSession = Depends(get_db)
):
    """Elimina la inscripción de un equipo en una temporada."""
    season_team = await season_repo.get_season_team(db, season_id, team_id)
    if not season_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El equipo no está inscrito en esta temporada")
    await season_repo.remove_team(db, season_team)
