from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.league import League
from app.models.match import Match, Round
from app.models.enums import MatchStatus
from app.models.season import Season, SeasonTeam
from app.models.team import Team
from app.models.tournament import PhaseGroup, Tournament, TournamentPhase


class FixtureImporter:
    """Importa jornadas y partidos de forma idempotente."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def import_file(self, path: Path) -> dict[str, int]:
        data = json.loads(path.read_text(encoding="utf-8"))
        return await self.import_data(data)

    async def import_data(self, data: dict[str, Any]) -> dict[str, int]:
        summary = {"rounds": 0, "matches": 0}

        league = await self._get_league(data["league"], data["country"])
        season = await self._get_season(league.id, data["season"])
        tournament = await self._get_tournament(season.id, data["tournament"])

        for round_data in data.get("rounds", []):
            phase = await self._get_phase(tournament.id, round_data["phase"])
            group = None
            if round_data.get("group"):
                group = await self._get_group(phase.id, round_data["group"])

            round_, created = await self._get_or_create_round(
                {
                    "phase_id": phase.id,
                    "group_id": group.id if group else None,
                    "number": round_data["number"],
                    "name": round_data["name"],
                    "date_start": _optional_date(round_data.get("date_start")),
                    "date_end": _optional_date(round_data.get("date_end")),
                }
            )
            summary["rounds"] += int(created)

            for match_data in round_data.get("matches", []):
                home_team = await self._get_team(match_data["home_team"])
                away_team = await self._get_team(match_data["away_team"])
                if home_team.id == away_team.id:
                    raise ValueError(f"Match has the same team twice: {home_team.name}")

                await self._validate_season_team(season.id, home_team.id)
                await self._validate_season_team(season.id, away_team.id)

                _, created = await self._get_or_create_match(
                    {
                        "round_id": round_.id,
                        "home_team_id": home_team.id,
                        "away_team_id": away_team.id,
                        "scheduled_datetime": _optional_datetime(
                            match_data.get("scheduled_datetime")
                        ),
                        "venue": match_data.get("venue"),
                        "status": MatchStatus(match_data.get("status", "scheduled")),
                        "home_score": match_data.get("home_score"),
                        "away_score": match_data.get("away_score"),
                    }
                )
                summary["matches"] += int(created)

        await self.session.commit()
        return summary

    async def _get_league(self, name: str, country: str) -> League:
        result = await self.session.execute(
            select(League).where(League.name == name, League.country == country)
        )
        league = result.scalar_one_or_none()
        if not league:
            raise ValueError(f"League not found: {name} ({country})")
        return league

    async def _get_season(self, league_id: Any, display_name: str) -> Season:
        result = await self.session.execute(
            select(Season).where(
                Season.league_id == league_id,
                Season.display_name == display_name,
            )
        )
        season = result.scalar_one_or_none()
        if not season:
            raise ValueError(f"Season not found: {display_name}")
        return season

    async def _get_tournament(self, season_id: Any, name: str) -> Tournament:
        result = await self.session.execute(
            select(Tournament).where(
                Tournament.season_id == season_id,
                Tournament.name == name,
            )
        )
        tournament = result.scalar_one_or_none()
        if not tournament:
            raise ValueError(f"Tournament not found: {name}")
        return tournament

    async def _get_phase(self, tournament_id: Any, name: str) -> TournamentPhase:
        result = await self.session.execute(
            select(TournamentPhase).where(
                TournamentPhase.tournament_id == tournament_id,
                TournamentPhase.name == name,
            )
        )
        phase = result.scalar_one_or_none()
        if not phase:
            raise ValueError(f"Phase not found: {name}")
        return phase

    async def _get_group(self, phase_id: Any, name: str) -> PhaseGroup:
        result = await self.session.execute(
            select(PhaseGroup).where(
                PhaseGroup.phase_id == phase_id,
                PhaseGroup.name == name,
            )
        )
        group = result.scalar_one_or_none()
        if not group:
            raise ValueError(f"Group not found: {name}")
        return group

    async def _get_team(self, name: str) -> Team:
        result = await self.session.execute(select(Team).where(Team.name == name))
        team = result.scalar_one_or_none()
        if not team:
            raise ValueError(f"Team not found: {name}")
        return team

    async def _validate_season_team(self, season_id: Any, team_id: Any) -> None:
        result = await self.session.execute(
            select(SeasonTeam).where(
                SeasonTeam.season_id == season_id,
                SeasonTeam.team_id == team_id,
            )
        )
        if not result.scalar_one_or_none():
            raise ValueError(f"Team {team_id} is not registered in season {season_id}")

    async def _get_or_create_round(self, data: dict[str, Any]) -> tuple[Round, bool]:
        query = select(Round).where(
            Round.phase_id == data["phase_id"],
            Round.number == data["number"],
        )
        if data["group_id"] is None:
            query = query.where(Round.group_id.is_(None))
        else:
            query = query.where(Round.group_id == data["group_id"])

        result = await self.session.execute(query)
        round_ = result.scalar_one_or_none()
        if round_:
            return round_, False

        round_ = Round(**data)
        self.session.add(round_)
        await self.session.flush()
        return round_, True

    async def _get_or_create_match(self, data: dict[str, Any]) -> tuple[Match, bool]:
        result = await self.session.execute(
            select(Match).where(
                Match.round_id == data["round_id"],
                Match.home_team_id == data["home_team_id"],
                Match.away_team_id == data["away_team_id"],
            )
        )
        match = result.scalar_one_or_none()
        if match:
            return match, False

        match = Match(**data)
        self.session.add(match)
        await self.session.flush()
        return match, True


def _optional_date(value: str | None) -> date | None:
    if value is None:
        return None
    return date.fromisoformat(value)


def _optional_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)
