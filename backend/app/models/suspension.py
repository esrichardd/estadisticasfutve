import uuid
from uuid import UUID

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
from app.models.enums import ScopeType


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

    NOTA: scope_id es una referencia polimórfica manual (puede apuntar a
    tournaments.id o tournament_phases.id según scope_type).
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
