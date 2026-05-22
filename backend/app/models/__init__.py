# Este archivo hace dos cosas importantes:
#
# 1. Re-exporta Base para que alembic/env.py pueda hacer:
#       from app.models import Base
#
# 2. Importa todos los modelos para que SQLAlchemy y Alembic los "vean".
#    Si un modelo no está importado aquí, Alembic no lo detecta en autogenerate.

from app.models.base import Base, TimestampMixin  # noqa: F401
from app.models.enums import (  # noqa: F401
    EventType,
    MatchStatus,
    PhaseType,
    RefereeRole,
    ScopeType,
)
from app.models.league import League  # noqa: F401
from app.models.match import Match, MatchEvent, MatchOfficial, Round  # noqa: F401
from app.models.player import Player, PlayerRegistration  # noqa: F401
from app.models.referee import Referee  # noqa: F401
from app.models.season import Season, SeasonTeam  # noqa: F401
from app.models.standing import Standing  # noqa: F401
from app.models.suspension import SuspensionCycle  # noqa: F401
from app.models.team import Team  # noqa: F401
from app.models.tournament import (  # noqa: F401
    GroupTeam,
    PhaseGroup,
    Tournament,
    TournamentPhase,
)
