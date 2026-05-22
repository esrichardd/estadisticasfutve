from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import standing_repo
from app.schemas.standing import StandingResponse

router = APIRouter(prefix="/standings", tags=["standings"])


@router.get("/", response_model=list[StandingResponse])
async def list_standings(
    phase_id: UUID | None = None,
    group_id: UUID | None = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """
    Lista posiciones ordenadas por puntos, diferencia de goles y goles a favor.
    Acepta filtro por fase y/o grupo.
    """
    return await standing_repo.get_all(
        db, phase_id=phase_id, group_id=group_id, limit=limit, offset=offset
    )


@router.get("/{standing_id}", response_model=StandingResponse)
async def get_standing(standing_id: UUID, db: AsyncSession = Depends(get_db)):
    """Devuelve el registro de posición de un equipo por su ID. 404 si no existe."""
    standing = await standing_repo.get_by_id(db, standing_id)
    if not standing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de posición no encontrado",
        )
    return standing
