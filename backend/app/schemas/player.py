from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, computed_field


class PlayerBase(BaseModel):
    name: str
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    position: Optional[str] = None


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    position: Optional[str] = None


class PlayerResponse(PlayerBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def age(self) -> Optional[int]:
        """Edad calculada al momento de la consulta."""
        if self.birth_date is None:
            return None
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    model_config = ConfigDict(from_attributes=True)


# ─── Registraciones ───────────────────────────────────────────────────────────


class PlayerRegistrationBase(BaseModel):
    player_id: UUID
    team_id: UUID
    season_id: UUID
    jersey_number: Optional[int] = None
    start_date: date
    end_date: Optional[date] = None
    is_loan: bool = False
    notes: Optional[str] = None


class PlayerRegistrationCreate(PlayerRegistrationBase):
    pass


class PlayerRegistrationUpdate(BaseModel):
    jersey_number: Optional[int] = None
    end_date: Optional[date] = None
    is_loan: Optional[bool] = None
    notes: Optional[str] = None


class PlayerRegistrationResponse(PlayerRegistrationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
