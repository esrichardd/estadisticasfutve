from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.config import settings

app = FastAPI(
    title="EstadisticasFutve API",
    description="API de estadísticas de la liga venezolana de fútbol",
    version="0.1.0",
)


def _custom_openapi():
    """Registra el esquema x-api-key en Swagger UI para que muestre el botón Authorize."""
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Fusiona securitySchemes con los components ya existentes (schemas de Pydantic, etc.)
    schema["components"] = {
        **schema.get("components", {}),
        "securitySchemes": {
            "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "x-api-key"}
        },
    }
    # Aplica el esquema globalmente — el health check lo muestra pero no lo enforcea
    # porque no tiene la dependencia verify_api_key.
    schema["security"] = [{"ApiKeyAuth": []}]
    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = _custom_openapi  # type: ignore[method-assign]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
from app.api.v1.router import router as v1_router

app.include_router(v1_router, prefix="/api/v1")


# ─── Health check ─────────────────────────────────────────────────────────────

@app.get("/", tags=["health"])
async def health_check():
    return {"status": "ok"}
