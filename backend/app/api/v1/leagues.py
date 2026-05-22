from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import league_repo
from app.schemas.league import LeagueCreate, LeagueResponse, LeagueUpdate

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get("/", response_model=list[LeagueResponse])
async def list_leagues(
    only_active: bool = False,
    country: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Lista todas las ligas. Acepta filtro por activas, por país y paginación."""
    return await league_repo.get_all(db, only_active=only_active, country=country, limit=limit, offset=offset)


@router.get("/{league_id}", response_model=LeagueResponse)
async def get_league(league_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve una liga por su ID. 404 si no existe."""
    league = await league_repo.get_by_id(db, league_id)
    if not league:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Liga no encontrada")
    return league


@router.post("/", response_model=LeagueResponse, status_code=status.HTTP_201_CREATED)
async def create_league(data: LeagueCreate, db: AsyncSession = Depends(get_db)):
    """Crea una nueva liga."""
    return await league_repo.create(db, data.model_dump())


@router.patch("/{league_id}", response_model=LeagueResponse)
async def update_league(league_id: UUID, data: LeagueUpdate, db: AsyncSession = Depends(get_db)):
    """Actualiza solo los campos enviados (PATCH semántico)."""
    league = await league_repo.get_by_id(db, league_id)
    if not league:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Liga no encontrada")
    return await league_repo.update(db, league, data.model_dump(exclude_none=True))
