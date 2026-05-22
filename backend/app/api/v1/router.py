from fastapi import APIRouter

from app.api.v1 import teams

# Router principal de v1 — agrega todos los sub-routers aquí.
# Para añadir un recurso nuevo: importarlo y agregar una línea include_router.
router = APIRouter()

router.include_router(teams.router)

# Próximos routers (se descomentan a medida que se implementan):
# from app.api.v1 import leagues, seasons, players, matches, standings
# router.include_router(leagues.router)
# router.include_router(seasons.router)
# router.include_router(players.router)
# router.include_router(matches.router)
# router.include_router(standings.router)
