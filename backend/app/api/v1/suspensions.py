from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import suspension_repo
from app.schemas.suspension import SuspensionCycleResponse, SuspensionCycleUpdate

router = APIRouter(prefix="/suspensions", tags=["suspensions"])


@router.get("/", response_model=list[SuspensionCycleResponse])
async def list_suspensions(
    player_id: UUID | None = None,
    is_suspended: bool | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    Lista ciclos de apercibido. Acepta filtro por jugador y/o estado de suspensión,
    y paginación.
    """
    return await suspension_repo.get_all(
        db, player_id=player_id, is_suspended=is_suspended, limit=limit, offset=offset
    )


@router.get("/{cycle_id}", response_model=SuspensionCycleResponse)
async def get_suspension(cycle_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve un ciclo de apercibido por su ID. 404 si no existe."""
    cycle = await suspension_repo.get_by_id(db, cycle_id)
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciclo de apercibido no encontrado",
        )
    return cycle


@router.patch("/{cycle_id}", response_model=SuspensionCycleResponse)
async def update_suspension(
    cycle_id: UUID, data: SuspensionCycleUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Actualiza un ciclo de apercibido. Solo permite marcar suspension_served como cumplida.
    404 si no existe.
    """
    cycle = await suspension_repo.get_by_id(db, cycle_id)
    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciclo de apercibido no encontrado",
        )
    return await suspension_repo.update(db, cycle, data.model_dump(exclude_none=True))
