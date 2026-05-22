from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.config import settings

# FastAPI lee automáticamente el header "x-api-key" de cada request.
# Si el header falta, devuelve 403 antes de llegar al endpoint.
_api_key_header = APIKeyHeader(name="x-api-key", auto_error=True)


async def verify_api_key(key: str = Security(_api_key_header)) -> str:
    """Dependencia reutilizable que valida el header x-api-key.

    Uso en un router completo:
        router = APIRouter(dependencies=[Depends(verify_api_key)])

    Uso en un endpoint individual:
        @router.get("/", dependencies=[Depends(verify_api_key)])
    """
    if key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key inválida",
        )
    return key
