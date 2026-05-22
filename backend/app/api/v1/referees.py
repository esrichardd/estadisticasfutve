from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import referee_repo
from app.schemas.referee import RefereeCreate, RefereeResponse, RefereeUpdate

router = APIRouter(prefix="/referees", tags=["referees"])


@router.get("/", response_model=list[RefereeResponse])
async def list_referees(
    only_active: bool = False,
    nationality: str | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Lista todos los árbitros. Acepta filtro por activos, por nacionalidad y paginación."""
    return await referee_repo.get_all(db, only_active=only_active, nationality=nationality, limit=limit, offset=offset)


@router.get("/{referee_id}", response_model=RefereeResponse)
async def get_referee(referee_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve un árbitro por su ID. 404 si no existe."""
    referee = await referee_repo.get_by_id(db, referee_id)
    if not referee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Árbitro no encontrado")
    return referee


@router.post("/", response_model=RefereeResponse, status_code=status.HTTP_201_CREATED)
async def create_referee(data: RefereeCreate, db: AsyncSession = Depends(get_db)):
    """Crea un nuevo árbitro."""
    return await referee_repo.create(db, data.model_dump())


@router.patch("/{referee_id}", response_model=RefereeResponse)
async def update_referee(referee_id: UUID, data: RefereeUpdate, db: AsyncSession = Depends(get_db)):
    """Actualiza solo los campos enviados (PATCH semántico)."""
    referee = await referee_repo.get_by_id(db, referee_id)
    if not referee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Árbitro no encontrado")
    return await referee_repo.update(db, referee, data.model_dump(exclude_none=True))
