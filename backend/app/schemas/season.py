from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SeasonBase(BaseModel):
    league_id: UUID
    display_name: str
    start_date: date
    end_date: date


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(BaseModel):
    display_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class SeasonResponse(SeasonBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─── Season Teams ─────────────────────────────────────────────────────────────


class SeasonTeamCreate(BaseModel):
    season_id: UUID
    team_id: UUID


class SeasonTeamResponse(SeasonTeamCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
