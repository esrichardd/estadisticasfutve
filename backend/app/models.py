"""
Modelos SQLAlchemy 2.0 para EstadisticasFutve.

Jerarquía de competencia:
    Liga → Temporada → Torneo → Fase → (Grupo) → Jornada → Partido → Evento

Tablas independientes : leagues, teams, players, referees
Nivel temporada       : seasons, season_teams, player_registrations
Estructura del torneo : tournaments, tournament_phases, phase_groups, group_teams
Partidos              : rounds, matches, match_officials, match_events
Derivadas             : standings, suspension_cycles
"""

import enum
import uuid
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# ─── Enums ────────────────────────────────────────────────────────────────────


class PhaseType(str, enum.Enum):
    """Tipo de fase dentro de un torneo."""

    round_robin = "round_robin"   # Todos contra todos (liga clásica)
    group_stage = "group_stage"   # Fase de grupos (varios round-robins en paralelo)
    knockout = "knockout"         # Eliminación directa (un solo partido)
    two_legged = "two_legged"     # Eliminación directa con ida y vuelta


class MatchStatus(str, enum.Enum):
    """Estado de un partido."""

    scheduled = "scheduled"   # Programado
    live = "live"             # En juego
    finished = "finished"     # Finalizado
    postponed = "postponed"   # Postergado
    cancelled = "cancelled"   # Cancelado


class RefereeRole(str, enum.Enum):
    """Rol de un árbitro en un partido."""

    main = "main"
    assistant_1 = "assistant_1"
    assistant_2 = "assistant_2"
    fourth_official = "fourth_official"
    var = "var"


class EventType(str, enum.Enum):
    """Tipo de evento registrado en un partido."""

    goal = "goal"                         # Gol
    own_goal = "own_goal"                 # Autogol
    assist = "assist"                     # Asistencia
    yellow_card = "yellow_card"           # Tarjeta amarilla
    second_yellow = "second_yellow"       # Segunda amarilla (implica expulsión)
    red_card = "red_card"                 # Roja directa
    substitution_in = "substitution_in"   # Jugador que entra
    substitution_out = "substitution_out" # Jugador que sale
    penalty_miss = "penalty_miss"         # Penalti fallado
    penalty_saved = "penalty_saved"       # Penalti atajado


class ScopeType(str, enum.Enum):
    """Ámbito de un ciclo de apercibido."""

    tournament = "tournament"  # El ciclo aplica a todo el torneo
    phase = "phase"            # El ciclo se reinicia por fase


# ─── Mixin de timestamps ──────────────────────────────────────────────────────


class TimestampMixin:
    """
    Agrega created_at y updated_at a cualquier modelo.

    created_at: se establece automáticamente al insertar (server_default=now()).
    updated_at: se establece al insertar y se actualiza al modificar via ORM
                (onupdate=func.now()). Para actualizaciones por SQL directo,
                se requeriría un trigger en PostgreSQL.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# ─── Entidades independientes ─────────────────────────────────────────────────


class League(TimestampMixin, Base):
    """
    Una liga o competición. Es la entidad raíz del sistema.
    Ejemplo: Primera División de Venezuela.
    """

    __tablename__ = "leagues"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    federation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<League id={self.id} name={self.name!r}>"


class Team(TimestampMixin, Base):
    """
    Un equipo de fútbol como entidad permanente, independiente de la temporada.
    Su participación por temporada se registra en SeasonTeam.
    """

    __tablename__ = "teams"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    short_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    abbreviation: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    stadium: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    founded_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Team id={self.id} name={self.name!r}>"


class Player(TimestampMixin, Base):
    """
    Un jugador como entidad permanente.
    Su vínculo con equipos y temporadas se gestiona en PlayerRegistration.
    """

    __tablename__ = "players"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    position: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    def __repr__(self) -> str:
        return f"<Player id={self.id} name={self.name!r}>"


class Referee(TimestampMixin, Base):
    """Árbitro que puede oficiar partidos."""

    __tablename__ = "referees"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Referee id={self.id} name={self.name!r}>"


# ─── Nivel Temporada ──────────────────────────────────────────────────────────


class Season(TimestampMixin, Base):
    """
    Una temporada dentro de una liga.
    Puede abarcar un solo año (2025) o cruzar dos años (2024-25).
    display_name es libre: '2025' o '2024-25'.
    """

    __tablename__ = "seasons"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    league_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("leagues.id"), nullable=False)
    display_name: Mapped[str] = mapped_column(String(20), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    def __repr__(self) -> str:
        return f"<Season id={self.id} display_name={self.display_name!r}>"


class SeasonTeam(TimestampMixin, Base):
    """
    Equipos participantes en una temporada.
    Necesario porque los equipos pueden ascender, descender o retirarse.
    Restricción: (season_id, team_id) es único.
    """

    __tablename__ = "season_teams"
    __table_args__ = (UniqueConstraint("season_id", "team_id", name="uq_season_team"),)

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    season_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("seasons.id"), nullable=False)
    team_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("teams.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<SeasonTeam season_id={self.season_id} team_id={self.team_id}>"


class PlayerRegistration(TimestampMixin, Base):
    """
    Historial de vínculos jugador–equipo por temporada.
    Permite rastrear transferencias y cesiones.

    IMPORTANTE: el team_id en MatchEvent se guarda siempre explícitamente
    en el evento y NUNCA se deriva de esta tabla, ya que el jugador pudo
    haberse transferido después del partido.
    """

    __tablename__ = "player_registrations"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    player_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("players.id"), nullable=False)
    team_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("teams.id"), nullable=False)
    season_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("seasons.id"), nullable=False)
    jersey_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)  # NULL = aún activo
    is_loan: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<PlayerRegistration player_id={self.player_id} team_id={self.team_id}>"


# ─── Estructura del Torneo ────────────────────────────────────────────────────


class Tournament(TimestampMixin, Base):
    """
    Un torneo dentro de una temporada.
    En Venezuela: Apertura (1), Clausura (2), Final Absoluta (3).
    El campo 'order' define el orden de disputa dentro de la temporada.
    """

    __tablename__ = "tournaments"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    season_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("seasons.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    def __repr__(self) -> str:
        return f"<Tournament id={self.id} name={self.name!r}>"


class TournamentPhase(TimestampMixin, Base):
    """
    Fase dentro de un torneo. Esta tabla es el núcleo de la flexibilidad
    del formato: define el tipo de fase, cuántas piernas tiene cada
    enfrentamiento y si el ciclo de apercibido se reinicia al iniciar.

    Ejemplo para el Apertura venezolano:
      - Ronda Regular  → round_robin, num_legs=1, cards_reset_on_start=False
      - Cuadrangulares → group_stage, num_legs=2, cards_reset_on_start=True
      - Final          → knockout,    num_legs=1, cards_reset_on_start=False
    """

    __tablename__ = "tournament_phases"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tournament_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("tournaments.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    phase_type: Mapped[PhaseType] = mapped_column(
        Enum(PhaseType, name="phase_type_enum"), nullable=False
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    num_legs: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    promotion_spots: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cards_reset_on_start: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    def __repr__(self) -> str:
        return f"<TournamentPhase id={self.id} name={self.name!r} type={self.phase_type}>"


class PhaseGroup(TimestampMixin, Base):
    """
    Grupo dentro de una fase de tipo group_stage.
    Ejemplo: Grupo A y Grupo B de los cuadrangulares.
    Las fases sin grupos simplemente no tienen registros aquí.
    """

    __tablename__ = "phase_groups"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    phase_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("tournament_phases.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<PhaseGroup id={self.id} name={self.name!r}>"


class GroupTeam(TimestampMixin, Base):
    """Asignación de un equipo a un grupo dentro de una fase."""

    __tablename__ = "group_teams"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    group_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("phase_groups.id"), nullable=False)
    team_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("teams.id"), nullable=False)
    seed: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<GroupTeam group_id={self.group_id} team_id={self.team_id}>"


# ─── Partidos ─────────────────────────────────────────────────────────────────


class Round(TimestampMixin, Base):
    """
    Jornada dentro de una fase (y opcionalmente de un grupo).
    Ejemplo: Jornada 1 de la Ronda Regular, Fecha 3 del Grupo A de Cuadrangulares.
    """

    __tablename__ = "rounds"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    phase_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("tournament_phases.id"), nullable=False)
    group_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid, ForeignKey("phase_groups.id"), nullable=True
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_start: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_end: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    def __repr__(self) -> str:
        return f"<Round id={self.id} name={self.name!r}>"


class Match(TimestampMixin, Base):
    """
    Un partido de fútbol.

    tie_id: agrupa los dos partidos de una eliminatoria de ida y vuelta.
            Permite calcular el marcador global sumando goles de ambos encuentros.

    leg: 1 = ida, 2 = vuelta. NULL si no es eliminatoria.

    reverse_of_match_id: en el Clausura, apunta al partido del Apertura
                         del que este es la vuelta (localía invertida).
    """

    __tablename__ = "matches"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    round_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("rounds.id"), nullable=False)
    home_team_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("teams.id"), nullable=False)
    away_team_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("teams.id"), nullable=False)
    tie_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    leg: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1=ida, 2=vuelta
    reverse_of_match_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid, ForeignKey("matches.id"), nullable=True
    )
    scheduled_datetime: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    venue: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    status: Mapped[MatchStatus] = mapped_column(
        Enum(MatchStatus, name="match_status_enum"),
        default=MatchStatus.scheduled,
        nullable=False,
    )
    home_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    away_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Match id={self.id} "
            f"home={self.home_team_id} away={self.away_team_id} "
            f"status={self.status}>"
        )


class MatchOfficial(TimestampMixin, Base):
    """Árbitros designados para un partido. Un partido tiene múltiples roles."""

    __tablename__ = "match_officials"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    match_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("matches.id"), nullable=False)
    referee_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("referees.id"), nullable=False)
    role: Mapped[RefereeRole] = mapped_column(
        Enum(RefereeRole, name="referee_role_enum"), nullable=False
    )

    def __repr__(self) -> str:
        return (
            f"<MatchOfficial match_id={self.match_id} "
            f"referee_id={self.referee_id} role={self.role}>"
        )


class MatchEvent(TimestampMixin, Base):
    """
    Evento ocurrido en un partido. Es la tabla más importante para estadísticas.
    Cada gol, tarjeta, asistencia o sustitución es un registro aquí con su minuto exacto.

    related_player_id: jugador secundario del evento.
        - En un gol: quién asistió.
        - En una sustitución_in: quién salió (y viceversa).

    team_id: equipo al que pertenecía el jugador EN ESE MOMENTO. Siempre
             explícito, nunca derivado de player_registrations.
    """

    __tablename__ = "match_events"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    match_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("matches.id"), nullable=False)
    player_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("players.id"), nullable=False)
    team_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("teams.id"), nullable=False)
    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType, name="event_type_enum"), nullable=False
    )
    minute: Mapped[int] = mapped_column(Integer, nullable=False)
    added_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    related_player_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid, ForeignKey("players.id"), nullable=True
    )

    def __repr__(self) -> str:
        return (
            f"<MatchEvent id={self.id} type={self.event_type} "
            f"minute={self.minute} player_id={self.player_id}>"
        )


# ─── Derivadas ────────────────────────────────────────────────────────────────


class Standing(TimestampMixin, Base):
    """
    Tabla de posiciones por fase y grupo. Vista desnormalizada que se actualiza
    al finalizar cada partido para evitar recalcular en cada consulta.
    Restricción: (phase_id, group_id, team_id) es único.
    """

    __tablename__ = "standings"
    __table_args__ = (
        UniqueConstraint("phase_id", "group_id", "team_id", name="uq_standing"),
    )

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    phase_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("tournament_phases.id"), nullable=False)
    group_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid, ForeignKey("phase_groups.id"), nullable=True
    )
    team_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("teams.id"), nullable=False)
    played: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    won: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    drawn: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lost: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    goals_for: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    goals_against: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    goal_difference: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )

    def __repr__(self) -> str:
        return (
            f"<Standing phase_id={self.phase_id} team_id={self.team_id} "
            f"pts={self.points}>"
        )


class SuspensionCycle(TimestampMixin, Base):
    """
    Ciclo de apercibido: seguimiento de amarillas que generan suspensiones.
    INDEPENDIENTE del conteo total de amarillas del año.

    Funcionamiento:
      1. yellow_count_in_cycle llega a threshold → is_suspended = True
      2. El jugador cumple su fecha → suspension_served = True
      3. Siguiente fecha: el ciclo se reinicia (count=0, cycle_number += 1)

    scope_type + scope_id definen el ámbito del ciclo:
      - 'tournament' + tournament_id: acumula en todo el torneo
      - 'phase' + phase_id: se reinicia al pasar de fase

    NOTA: scope_id es Integer porque es una referencia polimórfica manual
    (puede apuntar a tournaments.id o tournament_phases.id según scope_type).
    No tiene FK constraint a propósito.
    """

    __tablename__ = "suspension_cycles"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    player_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("players.id"), nullable=False)
    scope_type: Mapped[ScopeType] = mapped_column(
        Enum(ScopeType, name="scope_type_enum"), nullable=False
    )
    scope_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    yellow_count_in_cycle: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    threshold: Mapped[int] = mapped_column(Integer, default=4, nullable=False)
    is_suspended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    suspension_served: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cycle_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<SuspensionCycle player_id={self.player_id} "
            f"count={self.yellow_count_in_cycle}/{self.threshold} "
            f"suspended={self.is_suspended}>"
        )
