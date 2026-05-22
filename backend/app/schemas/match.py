from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import EventType, MatchStatus, RefereeRole


# ─── Rounds ───────────────────────────────────────────────────────────────────


class RoundBase(BaseModel):
    phase_id: UUID
    group_id: Optional[UUID] = None
    number: int
    name: str
    date_start: Optional[date] = None
    date_end: Optional[date] = None


class RoundCreate(RoundBase):
    pass


class RoundUpdate(BaseModel):
    name: Optional[str] = None
    date_start: Optional[date] = None
    date_end: Optional[date] = None


class RoundResponse(RoundBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─── Matches ──────────────────────────────────────────────────────────────────


class MatchBase(BaseModel):
    round_id: UUID
    home_team_id: UUID
    away_team_id: UUID
    tie_id: Optional[int] = None
    leg: Optional[int] = None
    reverse_of_match_id: Optional[UUID] = None
    scheduled_datetime: Optional[datetime] = None
    venue: Optional[str] = None
    status: MatchStatus = MatchStatus.scheduled


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    scheduled_datetime: Optional[datetime] = None
    venue: Optional[str] = None
    status: Optional[MatchStatus] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None


class MatchResponse(MatchBase):
    id: UUID
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─── Match Officials ──────────────────────────────────────────────────────────


class MatchOfficialCreate(BaseModel):
    match_id: UUID
    referee_id: UUID
    role: RefereeRole


class MatchOfficialResponse(MatchOfficialCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ─── Match Events ─────────────────────────────────────────────────────────────


class MatchEventBase(BaseModel):
    match_id: UUID
    player_id: UUID
    team_id: UUID
    event_type: EventType
    minute: int
    added_time: Optional[int] = None
    related_player_id: Optional[UUID] = None


class MatchEventCreate(MatchEventBase):
    pass


class MatchEventUpdate(BaseModel):
    minute: Optional[int] = None
    added_time: Optional[int] = None
    related_player_id: Optional[UUID] = None


class MatchEventResponse(MatchEventBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
