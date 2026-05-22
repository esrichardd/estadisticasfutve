import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


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
