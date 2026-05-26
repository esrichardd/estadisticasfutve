"""
Endpoints de vista para la home del frontend.

Arquitectura: Router → Repositorios → PostgreSQL
Sin lógica de negocio propia — solo orquestación de repositorios.

Temporada por defecto: 2026, Torneo: Apertura (Primera División de Venezuela).
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.views.home_mocks import LEADERS_MOCK
from app.database import get_db
from app.models.enums import MatchStatus, PhaseType
from app.repositories import (
    league_repo,
    match_repo,
    season_repo,
    standing_repo,
    team_repo,
    tournament_repo,
)
from app.schemas.views.home import (
    AttackHighlightSchema,
    DefenseHighlightSchema,
    GoalDiffHighlightSchema,
    HomeHighlightsResponse,
    HomeLeadersResponse,
    HomePhaseSchema,
    HomePhasesResponse,
    HomeRoundsGroupSchema,
    HomeRoundsResponse,
    HomeStandingHighlightSchema,
    HomeStandingRowSchema,
    HomeStandingsBracketResponse,
    HomeStandingsFinalistSchema,
    HomeStandingsGroupedTablesResponse,
    HomeStandingsGroupSchema,
    HomeStandingsSingleTableResponse,
    HomeSummaryResponse,
    SummaryCurrentRoundSchema,
    SummaryLeagueSchema,
    SummaryMetricsSchema,
    SummaryPhaseSchema,
    SummarySeasonSchema,
    SummaryTournamentSchema,
    TeamSummarySchema,
    _team_color,
)

router = APIRouter(prefix="/views/home", tags=["home-views"])


# ─── Helpers internos ─────────────────────────────────────────────────────────


def _build_team_summary(team) -> dict:
    """Construye el dict TeamSummary a partir de un objeto ORM Team."""
    return {
        "id": str(team.id),
        "name": team.name,
        "shortName": team.short_name or team.name,
        "abbreviation": team.abbreviation or "",
        "color": _team_color(str(team.id)),
        "logoUrl": team.logo_url,
    }


async def _calc_form(db, team_id, phase_id, limit: int = 5) -> list[str]:
    """
    Calcula la racha de forma reciente de un equipo en una fase.
    Devuelve una lista de hasta `limit` resultados en orden cronológico
    (el más reciente al final), con valores 'W', 'D' o 'L'.
    """
    recent = await match_repo.get_finished_matches_by_team(
        db, team_id=team_id, phase_id=phase_id, limit=limit
    )
    # get_finished_matches_by_team devuelve los partidos DESC; invertimos para
    # que el array vaya del más antiguo al más reciente.
    recent = list(reversed(recent))
    form = []
    for m in recent:
        if m.home_team_id == team_id:
            home, away = m.home_score or 0, m.away_score or 0
            form.append("W" if home > away else "D" if home == away else "L")
        else:
            home, away = m.home_score or 0, m.away_score or 0
            form.append("W" if away > home else "D" if away == home else "L")
    return form


async def _resolve_tournament(db, season_display: str, tournament_name: str):
    """
    Resuelve (league, season_obj, tournament_obj) a partir de los nombres.
    Lanza HTTPException 404 si alguno no se encuentra.
    """
    leagues = await league_repo.get_all(db)
    if not leagues:
        raise HTTPException(status_code=404, detail="No se encontró ninguna liga")
    league = leagues[0]  # Primera División de Venezuela es la única

    seasons = await season_repo.get_all(db, league_id=league.id)
    season_obj = next((s for s in seasons if s.display_name == season_display), None)
    if not season_obj:
        raise HTTPException(status_code=404, detail=f"Temporada '{season_display}' no encontrada")

    tournaments = await tournament_repo.get_tournaments(db, season_id=season_obj.id)
    tournament_obj = next((t for t in tournaments if t.name == tournament_name), None)
    if not tournament_obj:
        raise HTTPException(status_code=404, detail=f"Torneo '{tournament_name}' no encontrado")

    return league, season_obj, tournament_obj


async def _find_current_phase(db, phases: list) -> object:
    """
    Determina la fase actual iterando de mayor a menor order.
    Una fase es 'actual' si tiene al menos un round con algún match finished.
    Si ninguna cumple, devuelve la primera fase.
    """
    for phase in sorted(phases, key=lambda p: p.order, reverse=True):
        rounds = await match_repo.get_rounds(db, phase_id=phase.id)
        for round_ in rounds:
            matches = await match_repo.get_matches(db, round_id=round_.id)
            if any(m.status == MatchStatus.finished for m in matches):
                return phase
    return phases[0]


async def _build_home_round(db, round_) -> dict:
    """Construye el dict HomeRound con todos los partidos del round dado."""
    matches_raw = await match_repo.get_matches(db, round_id=round_.id)
    matches = []
    for m in matches_raw:
        home_team = await team_repo.get_by_id(db, m.home_team_id)
        away_team = await team_repo.get_by_id(db, m.away_team_id)
        scheduled = (
            m.scheduled_datetime.isoformat() if m.scheduled_datetime else ""
        )
        matches.append({
            "id": str(m.id),
            "status": m.status.value,
            "scheduledDatetime": scheduled,
            "venue": m.venue,
            "homeTeam": _build_team_summary(home_team),
            "awayTeam": _build_team_summary(away_team),
            "homeScore": m.home_score,
            "awayScore": m.away_score,
        })
    return {
        "id": str(round_.id),
        "number": round_.number,
        "name": round_.name,
        "dateStart": round_.date_start.isoformat() if round_.date_start else "",
        "dateEnd": round_.date_end.isoformat() if round_.date_end else "",
        "matches": matches,
    }


# ─── Endpoint 1: Summary ──────────────────────────────────────────────────────


@router.get("/summary", response_model=HomeSummaryResponse)
async def get_home_summary(
    season: str = "2026",
    tournament: str = "Apertura",
    db: AsyncSession = Depends(get_db),
):
    """
    Resumen general del torneo activo: liga, temporada, fase actual,
    jornada actual y métricas agregadas (líder, goles totales, próximo partido).
    """
    league, season_obj, tournament_obj = await _resolve_tournament(db, season, tournament)

    phases = await tournament_repo.get_phases(db, tournament_obj.id)
    if not phases:
        raise HTTPException(status_code=404, detail="El torneo no tiene fases definidas")

    current_phase = await _find_current_phase(db, phases)

    # Jornada actual: solo aplica en round_robin.
    # En group_stage hay múltiples grupos en paralelo, no hay una jornada única.
    current_round = None
    if current_phase.phase_type == PhaseType.round_robin:
        all_rounds = await match_repo.get_rounds(db, phase_id=current_phase.id)
        for round_ in sorted(all_rounds, key=lambda r: r.number, reverse=True):
            matches = await match_repo.get_matches(db, round_id=round_.id)
            if any(m.status == MatchStatus.finished for m in matches):
                current_round = round_
                break

    # Líder: equipo con más points en la fase round_robin (o la actual si no hay)
    leader_phase = next(
        (p for p in phases if p.phase_type == PhaseType.round_robin),
        current_phase,
    )

    # Métricas de conteo (total_goals, played_matches) → solo ronda regular
    # next_match_dt → todo el torneo (el próximo partido real, sea de cualquier fase)
    total_goals = 0
    played_matches = 0
    next_match_dt = None

    leader_phase_rounds = await match_repo.get_rounds(db, phase_id=leader_phase.id)
    for round_ in leader_phase_rounds:
        matches = await match_repo.get_matches(db, round_id=round_.id)
        for m in matches:
            if m.status == MatchStatus.finished:
                played_matches += 1
                total_goals += (m.home_score or 0) + (m.away_score or 0)

    for phase in phases:
        phase_rounds = await match_repo.get_rounds(db, phase_id=phase.id)
        for round_ in phase_rounds:
            matches = await match_repo.get_matches(db, round_id=round_.id)
            for m in matches:
                if m.status == MatchStatus.scheduled and m.scheduled_datetime:
                    if next_match_dt is None or m.scheduled_datetime < next_match_dt:
                        next_match_dt = m.scheduled_datetime

    next_match_str = next_match_dt.isoformat() if next_match_dt else ""
    leader_standings = await standing_repo.get_all(db, phase_id=leader_phase.id)
    leader_dict = {"teamName": "", "points": 0}
    if leader_standings:
        top = leader_standings[0]
        leader_team = await team_repo.get_by_id(db, top.team_id)
        leader_dict = {"teamName": leader_team.name, "points": top.points}

    # last_updated: standing más reciente del torneo
    last_updated = None
    all_standings = await standing_repo.get_all(db, phase_id=current_phase.id)
    for s in all_standings:
        if s.last_updated:
            if last_updated is None or s.last_updated > last_updated:
                last_updated = s.last_updated

    return HomeSummaryResponse(
        league=SummaryLeagueSchema(
            id=str(league.id),
            name=league.name,
            **{"logoUrl": getattr(league, "logo_url", None)},
        ),
        season=SummarySeasonSchema(
            id=str(season_obj.id),
            **{"displayName": season_obj.display_name},
        ),
        tournament=SummaryTournamentSchema(
            id=str(tournament_obj.id),
            name=tournament_obj.name,
        ),
        phase=SummaryPhaseSchema(
            id=str(current_phase.id),
            name=current_phase.name,
            type=current_phase.phase_type.value,
        ),
        **{"currentRound": SummaryCurrentRoundSchema(
            id=str(current_round.id),
            number=current_round.number,
            name=current_round.name,
        ) if current_round else None},
        metrics=SummaryMetricsSchema(
            leader=leader_dict,
            **{
                "totalGoals": total_goals,
                "playedMatches": played_matches,
                "nextMatch": next_match_str,
            },
        ),
        **{"lastUpdated": last_updated.isoformat() if last_updated else None},
    ).model_dump(by_alias=True)


# ─── Endpoint 2: Phases ───────────────────────────────────────────────────────


@router.get("/phases", response_model=HomePhasesResponse)
async def get_home_phases(
    season: str = "2026",
    tournament: str = "Apertura",
    db: AsyncSession = Depends(get_db),
):
    """
    Lista todas las fases del torneo con indicación de cuál es la actual.
    """
    _, _, tournament_obj = await _resolve_tournament(db, season, tournament)

    phases = await tournament_repo.get_phases(db, tournament_obj.id)
    if not phases:
        raise HTTPException(status_code=404, detail="El torneo no tiene fases definidas")

    current_phase = await _find_current_phase(db, phases)

    phase_list = [
        HomePhaseSchema(
            id=str(p.id),
            name=p.name,
            type=p.phase_type.value,
            **{"isCurrent": p.id == current_phase.id},
        )
        for p in phases
    ]

    return HomePhasesResponse(phases=phase_list).model_dump(by_alias=True)


# ─── Endpoint 3: Standings ────────────────────────────────────────────────────


@router.get("/standings")
async def get_home_standings(
    season: str = "2026",
    tournament: str = "Apertura",
    phase_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Tabla de posiciones de la fase indicada (o la actual si no se especifica).
    Devuelve viewType según el tipo de fase:
      - round_robin   → single_table
      - group_stage   → grouped_tables
      - knockout / two_legged → bracket
    """
    _, _, tournament_obj = await _resolve_tournament(db, season, tournament)

    phases = await tournament_repo.get_phases(db, tournament_obj.id)
    if not phases:
        raise HTTPException(status_code=404, detail="El torneo no tiene fases definidas")

    if phase_id is not None:
        phase = next((p for p in phases if p.id == phase_id), None)
        if not phase:
            raise HTTPException(status_code=404, detail=f"Fase '{phase_id}' no encontrada en este torneo")
    else:
        phase = await _find_current_phase(db, phases)

    # ── round_robin → single_table ──────────────────────────────────────────
    if phase.phase_type == PhaseType.round_robin:
        standings = await standing_repo.get_all(db, phase_id=phase.id)
        rows = []
        for i, s in enumerate(standings, start=1):
            team = await team_repo.get_by_id(db, s.team_id)
            form = await _calc_form(db, s.team_id, phase.id)
            rows.append(HomeStandingRowSchema(
                position=i,
                team=TeamSummarySchema(**_build_team_summary(team)),
                played=s.played,
                won=s.won,
                drawn=s.drawn,
                lost=s.lost,
                **{
                    "goalsFor": s.goals_for,
                    "goalsAgainst": s.goals_against,
                    "goalDifference": s.goal_difference,
                },
                points=s.points,
                form=form,
            ))

        highlights = [
            HomeStandingHighlightSchema(
                key="qualifiesKnockout",
                tone="promotion",
                **{"from": 1},
                to=8,
            )
        ]

        result = HomeStandingsSingleTableResponse(
            **{"phaseId": str(phase.id), "groupId": None, "viewType": "single_table"},
            rows=rows,
            highlights=highlights,
        )
        return result.model_dump(by_alias=True)

    # ── group_stage → grouped_tables ─────────────────────────────────────────
    if phase.phase_type == PhaseType.group_stage:
        groups = await tournament_repo.get_groups(db, phase.id)
        groups_data = []
        for group in groups:
            standings = await standing_repo.get_all(
                db, phase_id=phase.id, group_id=group.id
            )
            rows = []
            for i, s in enumerate(standings, start=1):
                team = await team_repo.get_by_id(db, s.team_id)
                form = await _calc_form(db, s.team_id, phase.id)
                rows.append(HomeStandingRowSchema(
                    position=i,
                    team=TeamSummarySchema(**_build_team_summary(team)),
                    played=s.played,
                    won=s.won,
                    drawn=s.drawn,
                    lost=s.lost,
                    **{
                        "goalsFor": s.goals_for,
                        "goalsAgainst": s.goals_against,
                        "goalDifference": s.goal_difference,
                    },
                    points=s.points,
                    form=form,
                ))
            groups_data.append(
                HomeStandingsGroupSchema(id=str(group.id), name=group.name, rows=rows)
            )

        highlights = [
            HomeStandingHighlightSchema(
                key="qualifiesFinal",
                tone="promotion",
                **{"from": 1},
                to=1,
            )
        ]

        result = HomeStandingsGroupedTablesResponse(
            **{"phaseId": str(phase.id), "groupId": None, "viewType": "grouped_tables"},
            groups=groups_data,
            highlights=highlights,
        )
        return result.model_dump(by_alias=True)

    # ── knockout / two_legged → bracket ──────────────────────────────────────
    group_stage_phase = next(
        (p for p in phases if p.phase_type == PhaseType.group_stage), None
    )
    finalist = None
    opponent = None

    if group_stage_phase:
        # Verificar si todos los partidos del group_stage están finalizados.
        # Mientras queden partidos pendientes, no proyectamos finalistas.
        group_stage_complete = True
        gs_rounds = await match_repo.get_rounds(db, phase_id=group_stage_phase.id)
        for gs_round in gs_rounds:
            gs_matches = await match_repo.get_matches(db, round_id=gs_round.id)
            if any(m.status != MatchStatus.finished for m in gs_matches):
                group_stage_complete = False
                break

        if group_stage_complete:
            groups = await tournament_repo.get_groups(db, group_stage_phase.id)
            for idx, group in enumerate(groups):
                standings = await standing_repo.get_all(
                    db, phase_id=group_stage_phase.id, group_id=group.id
                )
                if standings:
                    leader = standings[0]  # ya ordenado por points DESC
                    team = await team_repo.get_by_id(db, leader.team_id)
                    entry = HomeStandingsFinalistSchema(
                        **{
                            "teamId": str(team.id),
                            "teamName": team.name,
                            "fromGroupName": group.name,
                        }
                    )
                    if idx == 0:
                        finalist = entry
                    elif idx == 1:
                        opponent = entry

    result = HomeStandingsBracketResponse(
        **{"phaseId": str(phase.id), "groupId": None, "viewType": "bracket"},
        finalist=finalist,
        opponent=opponent,
        highlights=[],
    )
    return result.model_dump(by_alias=True)


# ─── Endpoint 4: Rounds ───────────────────────────────────────────────────────


@router.get("/rounds", response_model=HomeRoundsResponse)
async def get_home_rounds(
    season: str = "2026",
    tournament: str = "Apertura",
    db: AsyncSession = Depends(get_db),
):
    """
    Devuelve la jornada más reciente (latest) con partidos finalizados
    y la próxima jornada (next) con partidos programados.
    """
    _, _, tournament_obj = await _resolve_tournament(db, season, tournament)

    phases = await tournament_repo.get_phases(db, tournament_obj.id)
    if not phases:
        raise HTTPException(status_code=404, detail="El torneo no tiene fases definidas")

    import datetime as dt

    current_phase = await _find_current_phase(db, phases)

    def _pick_latest(rounds_with_matches):
        """Round más reciente con al menos un partido finished."""
        finished = [
            (r, m) for r, m in rounds_with_matches
            if any(match.status == MatchStatus.finished for match in m)
        ]
        if not finished:
            return None
        return max(
            finished,
            key=lambda rm: (rm[0].date_end or dt.date.min, rm[0].number),
        )[0]

    def _pick_next(rounds_with_matches):
        """Round más próximo con al menos un partido scheduled."""
        scheduled = [
            (r, m) for r, m in rounds_with_matches
            if any(match.status == MatchStatus.scheduled for match in m)
        ]
        if not scheduled:
            return None
        return min(
            scheduled,
            key=lambda rm: (rm[0].date_start or dt.date.max, rm[0].number),
        )[0]

    # ── group_stage → un latest/next por grupo ──────────────────────────────
    if current_phase.phase_type == PhaseType.group_stage:
        groups = await tournament_repo.get_groups(db, current_phase.id)
        groups_data = []
        for group in groups:
            group_rounds = await match_repo.get_rounds(
                db, phase_id=current_phase.id, group_id=group.id
            )
            rwm = []
            for round_ in group_rounds:
                matches = await match_repo.get_matches(db, round_id=round_.id)
                rwm.append((round_, matches))

            latest_r = _pick_latest(rwm)
            next_r = _pick_next(rwm)

            groups_data.append(HomeRoundsGroupSchema(**{
                "groupId": str(group.id),
                "groupName": group.name,
                "latest": await _build_home_round(db, latest_r) if latest_r else None,
                "next": await _build_home_round(db, next_r) if next_r else None,
            }))

        return HomeRoundsResponse(
            mode="grouped",
            groups=groups_data,
        ).model_dump(by_alias=True)

    # ── round_robin / knockout → latest y next únicos ───────────────────────
    all_rounds_with_matches = []
    for phase in phases:
        rounds = await match_repo.get_rounds(db, phase_id=phase.id)
        for round_ in rounds:
            matches = await match_repo.get_matches(db, round_id=round_.id)
            all_rounds_with_matches.append((round_, matches))

    latest_round = _pick_latest(all_rounds_with_matches)
    next_round = _pick_next(all_rounds_with_matches)

    latest_data = await _build_home_round(db, latest_round) if latest_round else None
    next_data = await _build_home_round(db, next_round) if next_round else None

    return HomeRoundsResponse(
        mode="single",
        latest=latest_data,
        next=next_data,
    ).model_dump(by_alias=True)


# ─── Endpoint 5: Highlights ───────────────────────────────────────────────────


@router.get("/highlights", response_model=HomeHighlightsResponse)
async def get_home_highlights(
    season: str = "2026",
    tournament: str = "Apertura",
    db: AsyncSession = Depends(get_db),
):
    """
    Highlights estadísticos del torneo: mejor ataque, mejor defensa y
    mejor diferencia de goles, calculados desde la fase round_robin.
    """
    _, _, tournament_obj = await _resolve_tournament(db, season, tournament)

    phases = await tournament_repo.get_phases(db, tournament_obj.id)
    if not phases:
        raise HTTPException(status_code=404, detail="El torneo no tiene fases definidas")

    # Usar la fase round_robin; si no existe, la primera que tenga standings
    highlight_phase = next(
        (p for p in phases if p.phase_type == PhaseType.round_robin), None
    )
    if highlight_phase is None:
        for p in phases:
            s = await standing_repo.get_all(db, phase_id=p.id)
            if s:
                highlight_phase = p
                break

    if not highlight_phase:
        return HomeHighlightsResponse(
            best_attack=None, best_defense=None, best_goal_difference=None
        ).model_dump(by_alias=True)

    standings = await standing_repo.get_all(db, phase_id=highlight_phase.id)
    if not standings:
        return HomeHighlightsResponse(
            best_attack=None, best_defense=None, best_goal_difference=None
        ).model_dump(by_alias=True)

    top_attack = max(standings, key=lambda s: s.goals_for)
    top_defense = min(standings, key=lambda s: s.goals_against)
    top_gd = max(standings, key=lambda s: s.goal_difference)

    attack_team = await team_repo.get_by_id(db, top_attack.team_id)
    defense_team = await team_repo.get_by_id(db, top_defense.team_id)
    gd_team = await team_repo.get_by_id(db, top_gd.team_id)

    return HomeHighlightsResponse(
        **{
            "bestAttack": AttackHighlightSchema(
                team=TeamSummarySchema(**_build_team_summary(attack_team)),
                **{"goalsFor": top_attack.goals_for},
            ),
            "bestDefense": DefenseHighlightSchema(
                team=TeamSummarySchema(**_build_team_summary(defense_team)),
                **{"goalsAgainst": top_defense.goals_against},
            ),
            "bestGoalDifference": GoalDiffHighlightSchema(
                team=TeamSummarySchema(**_build_team_summary(gd_team)),
                **{"goalDifference": top_gd.goal_difference},
            ),
        }
    ).model_dump(by_alias=True)


# ─── Endpoint 6: Leaders (mock temporal) ─────────────────────────────────────


@router.get("/leaders", response_model=HomeLeadersResponse)
async def get_home_leaders(
    season: str = "2026",
    tournament: str = "Apertura",
    db: AsyncSession = Depends(get_db),
):
    """
    TEMPORAL: devuelve listas vacías mientras match_events no esté poblada.
    Cuando se carguen eventos reales, reemplazar con queries a match_events
    filtrando por event_type IN ('goal', 'assist') para el torneo dado.
    El contrato del frontend no cambia.
    """
    return LEADERS_MOCK
