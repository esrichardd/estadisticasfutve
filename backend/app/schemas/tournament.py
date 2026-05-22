from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import PhaseType


class TournamentBase(BaseModel):
    season_id: UUID
    name: str
    order: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TournamentResponse(TournamentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─── Tournament Phases ────────────────────────────────────────────────────────


class TournamentPhaseBase(BaseModel):
    tournament_id: UUID
    name: str
    phase_type: PhaseType
    order: int
    num_legs: int = 1
    promotion_spots: Optional[int] = None
    cards_reset_on_start: bool = False


class TournamentPhaseCreate(TournamentPhaseBase):
    pass


class TournamentPhaseUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = None
    num_legs: Optional[int] = None
    promotion_spots: Optional[int] = None
    cards_reset_on_start: Optional[bool] = None


class TournamentPhaseResponse(TournamentPhaseBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─── Phase Groups ─────────────────────────────────────────────────────────────


class PhaseGroupCreate(BaseModel):
    phase_id: UUID
    name: str


class PhaseGroupUpdate(BaseModel):
    name: Optional[str] = None


class PhaseGroupResponse(PhaseGroupCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─── Group Teams ──────────────────────────────────────────────────────────────


class GroupTeamCreate(BaseModel):
    group_id: UUID
    team_id: UUID
    seed: Optional[int] = None


class GroupTeamResponse(GroupTeamCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
