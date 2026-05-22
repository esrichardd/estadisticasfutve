from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Usuario

# ─── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="API de Usuarios",
    description="CRUD de usuarios con FastAPI + SQLAlchemy async + PostgreSQL",
    version="1.0.0",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Schemas Pydantic ─────────────────────────────────────────────────────────


class UsuarioCreate(BaseModel):
    name: str
    lastname: str
    email: EmailStr


class UsuarioUpdate(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None


class UsuarioResponse(BaseModel):
    id: int
    name: str
    lastname: str
    email: str

    model_config = {"from_attributes": True}


# ─── Endpoints ────────────────────────────────────────────────────────────────


@app.get("/", summary="Health check")
async def root():
    return {"status": "ok", "message": "Hello World"}


@app.get(
    "/usuarios",
    response_model=list[UsuarioResponse],
    summary="Listar todos los usuarios",
)
async def get_usuarios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).order_by(Usuario.id))
    return result.scalars().all()


@app.get(
    "/usuarios/{id}",
    response_model=UsuarioResponse,
    summary="Obtener un usuario por ID",
)
async def get_usuario(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id == id))
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={id} no encontrado",
        )
    return usuario


@app.post(
    "/usuarios",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
)
async def create_usuario(data: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    usuario = Usuario(**data.model_dump())
    db.add(usuario)
    try:
        await db.commit()
        await db.refresh(usuario)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un usuario con el email '{data.email}'",
        )
    return usuario


@app.put(
    "/usuarios/{id}",
    response_model=UsuarioResponse,
    summary="Actualizar un usuario",
)
async def update_usuario(
    id: int, data: UsuarioUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Usuario).where(Usuario.id == id))
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={id} no encontrado",
        )
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(usuario, field, value)
    try:
        await db.commit()
        await db.refresh(usuario)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está en uso por otro usuario",
        )
    return usuario


@app.delete(
    "/usuarios/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
)
async def delete_usuario(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id == id))
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={id} no encontrado",
        )
    await db.delete(usuario)
    await db.commit()
