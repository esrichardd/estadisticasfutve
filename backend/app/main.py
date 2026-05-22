from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(
    title="EstadisticasFutve API",
    description="API de estadísticas de la liga venezolana de fútbol",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
# Se registran aquí a medida que se van creando:
#   from app.api.v1.router import router as v1_router
#   app.include_router(v1_router, prefix="/api/v1")


# ─── Health check ─────────────────────────────────────────────────────────────

@app.get("/", tags=["health"])
async def health_check():
    return {"status": "ok"}
