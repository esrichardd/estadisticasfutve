from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import ScopeType


class SuspensionCycleResponse(BaseModel):
    """
    Los ciclos de apercibido no se crean manualmente — se generan
    automáticamente al registrar tarjetas amarillas. Solo se pueden
    consultar y marcar como cumplidos.
    """

    id: UUID
    player_id: UUID
    scope_type: ScopeType
    scope_id: UUID
    yellow_count_in_cycle: int
    threshold: int
    is_suspended: bool
    suspension_served: bool
    cycle_number: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SuspensionCycleUpdate(BaseModel):
    """Solo permite marcar una suspensión como cumplida."""

    suspension_served: Optional[bool] = None
