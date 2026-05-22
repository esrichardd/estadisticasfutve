import uuid
from datetime import date
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


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
