import uuid
from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


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
