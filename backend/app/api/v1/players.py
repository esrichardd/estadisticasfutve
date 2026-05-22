from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import player_repo
from app.schemas.player import PlayerCreate, PlayerResponse, PlayerUpdate

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", response_model=list[PlayerResponse])
async def list_players(
    position: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Lista todos los jugadores. Acepta filtro por posición y paginación."""
    return await player_repo.get_all(db, position=position, limit=limit, offset=offset)


@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve un jugador por su ID. 404 si no existe."""
    player = await player_repo.get_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return player


@router.post("/", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
async def create_player(data: PlayerCreate, db: AsyncSession = Depends(get_db)):
    """Crea un nuevo jugador."""
    return await player_repo.create(db, data.model_dump())


@router.patch("/{player_id}", response_model=PlayerResponse)
async def update_player(player_id: UUID, data: PlayerUpdate, db: AsyncSession = Depends(get_db)):
    """Actualiza solo los campos enviados (PATCH semántico)."""
    player = await player_repo.get_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return await player_repo.update(db, player, data.model_dump(exclude_none=True))
