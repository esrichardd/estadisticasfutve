from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StandingResponse(BaseModel):
    """
    Las posiciones no se crean ni editan directamente via API —
    se recalculan automáticamente al finalizar cada partido.
    Por eso solo existe el schema de respuesta.
    """

    id: UUID
    phase_id: UUID
    group_id: Optional[UUID] = None
    team_id: UUID
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    last_updated: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
