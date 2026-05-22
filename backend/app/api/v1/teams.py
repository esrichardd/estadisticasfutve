from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import team_repo
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[TeamResponse])
async def list_teams(
    only_active: bool = False,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Lista todos los equipos. Acepta filtro por activos y paginación."""
    return await team_repo.get_all(db, only_active=only_active, limit=limit, offset=offset)


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve un equipo por su ID. 404 si no existe."""
    team = await team_repo.get_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return team


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(data: TeamCreate, db: AsyncSession = Depends(get_db)):
    """Crea un nuevo equipo."""
    return await team_repo.create(db, data.model_dump())


@router.patch("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: UUID, data: TeamUpdate, db: AsyncSession = Depends(get_db)):
    """Actualiza solo los campos enviados (PATCH semántico)."""
    team = await team_repo.get_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return await team_repo.update(db, team, data.model_dump(exclude_none=True))
