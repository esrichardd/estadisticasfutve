import uuid
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
from app.models.enums import EventType, MatchStatus, RefereeRole


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
