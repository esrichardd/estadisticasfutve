from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import MatchStatus, PhaseType
from app.models.league import League
from app.models.match import Match, Round
from app.models.season import Season
from app.models.standing import Standing
from app.models.tournament import PhaseGroup, Tournament, TournamentPhase


@dataclass
class StandingTotals:
    team_id: Any
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against


class StandingsRecalculator:
    """Recalcula standings desde partidos finalizados."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def recalculate_tournament(
        self,
        *,
        league_name: str,
        country: str,
        season_name: str,
        tournament_name: str,
        include_knockout: bool = False,
    ) -> dict[str, int]:
        league = await self._get_league(league_name, country)
        season = await self._get_season(league.id, season_name)
        tournament = await self._get_tournament(season.id, tournament_name)
        phases = await self._get_phases(tournament.id)

        summary = {"phases": 0, "groups": 0, "standings": 0}
        for phase in phases:
            if phase.phase_type == PhaseType.knockout and not include_knockout:
                continue

            groups = await self._get_groups(phase.id)
            if groups:
                for group in groups:
                    count = await self._recalculate_scope(phase, group)
                    summary["groups"] += 1
                    summary["standings"] += count
            else:
                count = await self._recalculate_scope(phase, None)
                summary["standings"] += count

            summary["phases"] += 1

        await self.session.commit()
        return summary

    async def _recalculate_scope(
        self, phase: TournamentPhase, group: PhaseGroup | None
    ) -> int:
        matches = await self._get_finished_matches(phase.id, group.id if group else None)
        totals: dict[Any, StandingTotals] = {}

        for match in matches:
            if match.home_score is None or match.away_score is None:
                raise ValueError(f"Finished match {match.id} has no score")

            home = totals.setdefault(match.home_team_id, StandingTotals(match.home_team_id))
            away = totals.setdefault(match.away_team_id, StandingTotals(match.away_team_id))

            home.played += 1
            away.played += 1
            home.goals_for += match.home_score
            home.goals_against += match.away_score
            away.goals_for += match.away_score
            away.goals_against += match.home_score

            if match.home_score > match.away_score:
                home.won += 1
                home.points += 3
                away.lost += 1
            elif match.home_score < match.away_score:
                away.won += 1
                away.points += 3
                home.lost += 1
            else:
                home.drawn += 1
                away.drawn += 1
                home.points += 1
                away.points += 1

        count = 0
        for totals_row in totals.values():
            standing = await self._get_or_create_standing(
                phase.id, group.id if group else None, totals_row.team_id
            )
            standing.played = totals_row.played
            standing.won = totals_row.won
            standing.drawn = totals_row.drawn
            standing.lost = totals_row.lost
            standing.goals_for = totals_row.goals_for
            standing.goals_against = totals_row.goals_against
            standing.goal_difference = totals_row.goal_difference
            standing.points = totals_row.points
            count += 1

        return count

    async def _get_finished_matches(self, phase_id: Any, group_id: Any | None) -> list[Match]:
        query = (
            select(Match)
            .join(Round, Match.round_id == Round.id)
            .where(
                Round.phase_id == phase_id,
                Match.status == MatchStatus.finished,
            )
        )
        if group_id is None:
            query = query.where(Round.group_id.is_(None))
        else:
            query = query.where(Round.group_id == group_id)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def _get_or_create_standing(
        self, phase_id: Any, group_id: Any | None, team_id: Any
    ) -> Standing:
        query = select(Standing).where(
            Standing.phase_id == phase_id,
            Standing.team_id == team_id,
        )
        if group_id is None:
            query = query.where(Standing.group_id.is_(None))
        else:
            query = query.where(Standing.group_id == group_id)

        result = await self.session.execute(query)
        standing = result.scalar_one_or_none()
        if standing:
            return standing

        standing = Standing(phase_id=phase_id, group_id=group_id, team_id=team_id)
        self.session.add(standing)
        await self.session.flush()
        return standing

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

    async def _get_phases(self, tournament_id: Any) -> list[TournamentPhase]:
        result = await self.session.execute(
            select(TournamentPhase)
            .where(TournamentPhase.tournament_id == tournament_id)
            .order_by(TournamentPhase.order)
        )
        return list(result.scalars().all())

    async def _get_groups(self, phase_id: Any) -> list[PhaseGroup]:
        result = await self.session.execute(
            select(PhaseGroup).where(PhaseGroup.phase_id == phase_id).order_by(PhaseGroup.name)
        )
        return list(result.scalars().all())
