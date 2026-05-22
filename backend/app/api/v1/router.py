from fastapi import APIRouter, Security

from app.api.v1 import leagues, matches, players, referees, seasons, standings, suspensions, teams, tournaments
from app.dependencies.auth import verify_api_key

# Router principal de v1 — todos los endpoints bajo /api/v1 requieren x-api-key.
# Security (en lugar de Depends) hace que FastAPI incluya el esquema en OpenAPI
# y muestre el botón "Authorize" en Swagger UI.
router = APIRouter(dependencies=[Security(verify_api_key)])

router.include_router(leagues.router)
router.include_router(matches.router)
router.include_router(players.router)
router.include_router(referees.router)
router.include_router(seasons.router)
router.include_router(standings.router)
router.include_router(suspensions.router)
router.include_router(teams.router)
router.include_router(tournaments.router)

