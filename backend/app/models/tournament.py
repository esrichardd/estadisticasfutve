import uuid
from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
from app.models.enums import PhaseType


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
    cards_reset_on_start: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

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
