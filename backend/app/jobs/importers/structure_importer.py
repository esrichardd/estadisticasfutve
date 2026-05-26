from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import PhaseType
from app.models.league import League
from app.models.season import Season, SeasonTeam
from app.models.team import Team
from app.models.tournament import GroupTeam, PhaseGroup, Tournament, TournamentPhase


class StructureImporter:
    """Importa estructura de liga/temporada/torneo de forma idempotente."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def import_file(self, path: Path) -> dict[str, int]:
        data = json.loads(path.read_text(encoding="utf-8"))
        return await self.import_data(data)

    async def import_data(self, data: dict[str, Any]) -> dict[str, int]:
        summary = {
            "leagues": 0,
            "seasons": 0,
            "teams": 0,
            "season_teams": 0,
            "tournaments": 0,
            "phases": 0,
            "groups": 0,
            "group_teams": 0,
        }

        league, created = await self._get_or_create_league(data["league"])
        summary["leagues"] += int(created)

        season_data = {
            **data["season"],
            "league_id": league.id,
        }
        season, created = await self._get_or_create_season(season_data)
        summary["seasons"] += int(created)

        teams_by_name: dict[str, Team] = {}
        for team_data in data.get("teams", []):
            team, created = await self._get_or_create_team(team_data)
            summary["teams"] += int(created)
            teams_by_name[team.name] = team

            _, created = await self._get_or_create_season_team(season.id, team.id)
            summary["season_teams"] += int(created)

        for tournament_data in data.get("tournaments", []):
            tournament_payload = {
                key: value
                for key, value in tournament_data.items()
                if key != "phases"
            }
            tournament_payload["season_id"] = season.id
            tournament, created = await self._get_or_create_tournament(tournament_payload)
            summary["tournaments"] += int(created)

            for phase_data in tournament_data.get("phases", []):
                phase_payload = {
                    key: value
                    for key, value in phase_data.items()
                    if key != "groups"
                }
                phase_payload["tournament_id"] = tournament.id
                phase, created = await self._get_or_create_phase(phase_payload)
                summary["phases"] += int(created)

                for group_data in phase_data.get("groups", []):
                    group, created = await self._get_or_create_group(
                        {"phase_id": phase.id, "name": group_data["name"]}
                    )
                    summary["groups"] += int(created)

                    for group_team_data in group_data.get("teams", []):
                        team = teams_by_name.get(group_team_data["name"])
                        if team is None:
                            raise ValueError(
                                "Group team is not declared in teams list: "
                                f"{group_team_data['name']}"
                            )
                        _, created = await self._get_or_create_group_team(
                            {
                                "group_id": group.id,
                                "team_id": team.id,
                                "seed": group_team_data.get("seed"),
                            }
                        )
                        summary["group_teams"] += int(created)

        await self.session.commit()
        return summary

    async def _get_or_create_league(self, data: dict[str, Any]) -> tuple[League, bool]:
        result = await self.session.execute(
            select(League).where(
                League.name == data["name"],
                League.country == data["country"],
            )
        )
        league = result.scalar_one_or_none()
        if league:
            return league, False

        league = League(**data)
        self.session.add(league)
        await self.session.flush()
        return league, True

    async def _get_or_create_season(self, data: dict[str, Any]) -> tuple[Season, bool]:
        result = await self.session.execute(
            select(Season).where(
                Season.league_id == data["league_id"],
                Season.display_name == data["display_name"],
            )
        )
        season = result.scalar_one_or_none()
        if season:
            return season, False

        season = Season(
            league_id=data["league_id"],
            display_name=data["display_name"],
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"]),
        )
        self.session.add(season)
        await self.session.flush()
        return season, True

    async def _get_or_create_team(self, data: dict[str, Any]) -> tuple[Team, bool]:
        result = await self.session.execute(select(Team).where(Team.name == data["name"]))
        team = result.scalar_one_or_none()
        if team:
            return team, False

        team = Team(**data)
        self.session.add(team)
        await self.session.flush()
        return team, True

    async def _get_or_create_season_team(
        self, season_id: Any, team_id: Any
    ) -> tuple[SeasonTeam, bool]:
        result = await self.session.execute(
            select(SeasonTeam).where(
                SeasonTeam.season_id == season_id,
                SeasonTeam.team_id == team_id,
            )
        )
        season_team = result.scalar_one_or_none()
        if season_team:
            return season_team, False

        season_team = SeasonTeam(season_id=season_id, team_id=team_id)
        self.session.add(season_team)
        await self.session.flush()
        return season_team, True

    async def _get_or_create_tournament(
        self, data: dict[str, Any]
    ) -> tuple[Tournament, bool]:
        result = await self.session.execute(
            select(Tournament).where(
                Tournament.season_id == data["season_id"],
                Tournament.name == data["name"],
            )
        )
        tournament = result.scalar_one_or_none()
        if tournament:
            return tournament, False

        tournament = Tournament(
            season_id=data["season_id"],
            name=data["name"],
            order=data["order"],
            start_date=_optional_date(data.get("start_date")),
            end_date=_optional_date(data.get("end_date")),
        )
        self.session.add(tournament)
        await self.session.flush()
        return tournament, True

    async def _get_or_create_phase(
        self, data: dict[str, Any]
    ) -> tuple[TournamentPhase, bool]:
        result = await self.session.execute(
            select(TournamentPhase).where(
                TournamentPhase.tournament_id == data["tournament_id"],
                TournamentPhase.name == data["name"],
            )
        )
        phase = result.scalar_one_or_none()
        if phase:
            return phase, False

        phase = TournamentPhase(
            tournament_id=data["tournament_id"],
            name=data["name"],
            phase_type=PhaseType(data["phase_type"]),
            order=data["order"],
            num_legs=data.get("num_legs", 1),
            promotion_spots=data.get("promotion_spots"),
            cards_reset_on_start=data.get("cards_reset_on_start", False),
        )
        self.session.add(phase)
        await self.session.flush()
        return phase, True

    async def _get_or_create_group(
        self, data: dict[str, Any]
    ) -> tuple[PhaseGroup, bool]:
        result = await self.session.execute(
            select(PhaseGroup).where(
                PhaseGroup.phase_id == data["phase_id"],
                PhaseGroup.name == data["name"],
            )
        )
        group = result.scalar_one_or_none()
        if group:
            return group, False

        group = PhaseGroup(**data)
        self.session.add(group)
        await self.session.flush()
        return group, True

    async def _get_or_create_group_team(
        self, data: dict[str, Any]
    ) -> tuple[GroupTeam, bool]:
        result = await self.session.execute(
            select(GroupTeam).where(
                GroupTeam.group_id == data["group_id"],
                GroupTeam.team_id == data["team_id"],
            )
        )
        group_team = result.scalar_one_or_none()
        if group_team:
            return group_team, False

        group_team = GroupTeam(**data)
        self.session.add(group_team)
        await self.session.flush()
        return group_team, True


def _optional_date(value: str | None) -> date | None:
    if value is None:
        return None
    return date.fromisoformat(value)
