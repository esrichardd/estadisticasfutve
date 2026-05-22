from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos SQLAlchemy."""
    pass


class TimestampMixin:
    """
    Agrega created_at y updated_at a cualquier modelo.

    created_at: se establece automáticamente al insertar (server_default=now()).
    updated_at: se actualiza al modificar via ORM (onupdate=func.now()).
                Para actualizaciones por SQL directo se requeriría un trigger.
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
