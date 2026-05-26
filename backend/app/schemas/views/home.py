"""
Schemas Pydantic para los endpoints de vista de la home.

Todos los campos siguen el contrato TypeScript del frontend:
los nombres Python usan snake_case pero se serializan en camelCase
mediante alias y by_alias=True en el endpoint.
"""

import hashlib
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ─── Color determinístico ──────────────────────────────────────────────────────

# Paleta de colores sport-appropriate (12 opciones)
_TEAM_COLORS = [
    "#E63946", "#2196F3", "#4CAF50", "#FF9800",
    "#9C27B0", "#00BCD4", "#F44336", "#3F51B5",
    "#009688", "#FF5722", "#607D8B", "#795548",
]


def _team_color(team_id: str) -> str:
    """Genera un color CSS determinístico a partir del UUID del equipo."""
    digest = hashlib.md5(team_id.encode()).hexdigest()
    index = int(digest[:4], 16) % len(_TEAM_COLORS)
    return _TEAM_COLORS[index]


# ─── Shared ───────────────────────────────────────────────────────────────────

class TeamSummarySchema(BaseModel):
    id: str
    name: str
    short_name: str = Field(alias="shortName")
    abbreviation: str
    color: str
    logo_url: Optional[str] = Field(None, alias="logoUrl")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# ─── Summary ──────────────────────────────────────────────────────────────────

class SummaryLeagueSchema(BaseModel):
    id: str
    name: str
    logo_url: Optional[str] = Field(None, alias="logoUrl")

    model_config = ConfigDict(populate_by_name=True)


class SummarySeasonSchema(BaseModel):
    id: str
    display_name: str = Field(alias="displayName")

    model_config = ConfigDict(populate_by_name=True)


class SummaryTournamentSchema(BaseModel):
    id: str
    name: str


class SummaryPhaseSchema(BaseModel):
    id: str
    name: str
    type: str  # PhaseType value


class SummaryCurrentRoundSchema(BaseModel):
    id: str
    number: int
    name: str


class SummaryMetricsSchema(BaseModel):
    leader: dict  # { "teamName": str, "points": int }
    total_goals: int = Field(alias="totalGoals")
    played_matches: int = Field(alias="playedMatches")
    next_match: str = Field(alias="nextMatch")  # ISO UTC string o ""

    model_config = ConfigDict(populate_by_name=True)


class HomeSummaryResponse(BaseModel):
    league: SummaryLeagueSchema
    season: SummarySeasonSchema
    tournament: SummaryTournamentSchema
    phase: SummaryPhaseSchema
    current_round: Optional[SummaryCurrentRoundSchema] = Field(None, alias="currentRound")
    metrics: SummaryMetricsSchema
    last_updated: Optional[str] = Field(None, alias="lastUpdated")

    model_config = ConfigDict(populate_by_name=True)


# ─── Phases ───────────────────────────────────────────────────────────────────

class HomePhaseSchema(BaseModel):
    id: str
    name: str
    type: str
    is_current: bool = Field(alias="isCurrent")

    model_config = ConfigDict(populate_by_name=True)


class HomePhasesResponse(BaseModel):
    phases: list[HomePhaseSchema]


# ─── Standings ────────────────────────────────────────────────────────────────

class HomeStandingRowSchema(BaseModel):
    position: int
    team: TeamSummarySchema
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int = Field(alias="goalsFor")
    goals_against: int = Field(alias="goalsAgainst")
    goal_difference: int = Field(alias="goalDifference")
    points: int
    form: list = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)


class HomeStandingHighlightSchema(BaseModel):
    key: str
    tone: str
    from_: int = Field(alias="from")
    to: Optional[int] = None

    model_config = ConfigDict(populate_by_name=True)


class HomeStandingsGroupSchema(BaseModel):
    id: str
    name: str
    rows: list[HomeStandingRowSchema]


class HomeStandingsFinalistSchema(BaseModel):
    team_id: str = Field(alias="teamId")
    team_name: str = Field(alias="teamName")
    from_group_name: str = Field(alias="fromGroupName")

    model_config = ConfigDict(populate_by_name=True)


# Tres variantes de respuesta según viewType:
class HomeStandingsSingleTableResponse(BaseModel):
    phase_id: str = Field(alias="phaseId")
    group_id: None = Field(None, alias="groupId")
    view_type: str = Field("single_table", alias="viewType")
    rows: list[HomeStandingRowSchema]
    highlights: list[HomeStandingHighlightSchema]

    model_config = ConfigDict(populate_by_name=True)


class HomeStandingsGroupedTablesResponse(BaseModel):
    phase_id: str = Field(alias="phaseId")
    group_id: None = Field(None, alias="groupId")
    view_type: str = Field("grouped_tables", alias="viewType")
    groups: list[HomeStandingsGroupSchema]
    highlights: list[HomeStandingHighlightSchema]

    model_config = ConfigDict(populate_by_name=True)


class HomeStandingsBracketResponse(BaseModel):
    phase_id: str = Field(alias="phaseId")
    group_id: None = Field(None, alias="groupId")
    view_type: str = Field("bracket", alias="viewType")
    finalist: Optional[HomeStandingsFinalistSchema] = None
    opponent: Optional[HomeStandingsFinalistSchema] = None
    highlights: list = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)


# Union type para serialización manual en el endpoint:
HomeStandingsResponse = (
    HomeStandingsSingleTableResponse
    | HomeStandingsGroupedTablesResponse
    | HomeStandingsBracketResponse
)


# ─── Rounds ───────────────────────────────────────────────────────────────────

class HomeMatchSchema(BaseModel):
    id: str
    status: str
    scheduled_datetime: str = Field(alias="scheduledDatetime")
    venue: Optional[str] = None
    home_team: TeamSummarySchema = Field(alias="homeTeam")
    away_team: TeamSummarySchema = Field(alias="awayTeam")
    home_score: Optional[int] = Field(None, alias="homeScore")
    away_score: Optional[int] = Field(None, alias="awayScore")

    model_config = ConfigDict(populate_by_name=True)


class HomeRoundSchema(BaseModel):
    id: str
    number: int
    name: str
    date_start: str = Field(alias="dateStart")
    date_end: str = Field(alias="dateEnd")
    matches: list[HomeMatchSchema]

    model_config = ConfigDict(populate_by_name=True)


class HomeRoundsResponse(BaseModel):
    latest: Optional[HomeRoundSchema] = None
    next: Optional[HomeRoundSchema] = None


# ─── Highlights ───────────────────────────────────────────────────────────────

class AttackHighlightSchema(BaseModel):
    team: TeamSummarySchema
    goals_for: int = Field(alias="goalsFor")

    model_config = ConfigDict(populate_by_name=True)


class DefenseHighlightSchema(BaseModel):
    team: TeamSummarySchema
    goals_against: int = Field(alias="goalsAgainst")

    model_config = ConfigDict(populate_by_name=True)


class GoalDiffHighlightSchema(BaseModel):
    team: TeamSummarySchema
    goal_difference: int = Field(alias="goalDifference")

    model_config = ConfigDict(populate_by_name=True)


class HomeHighlightsResponse(BaseModel):
    best_attack: Optional[AttackHighlightSchema] = Field(None, alias="bestAttack")
    best_defense: Optional[DefenseHighlightSchema] = Field(None, alias="bestDefense")
    best_goal_difference: Optional[GoalDiffHighlightSchema] = Field(None, alias="bestGoalDifference")

    model_config = ConfigDict(populate_by_name=True)


# ─── Leaders (mock temporal) ──────────────────────────────────────────────────

class PlayerSummarySchema(BaseModel):
    id: str
    name: str
    position: Optional[str] = None


class PlayerLeaderSchema(BaseModel):
    player: PlayerSummarySchema
    team: TeamSummarySchema
    value: int


class HomeLeadersResponse(BaseModel):
    scorers: list[PlayerLeaderSchema]
    assisters: list[PlayerLeaderSchema]
