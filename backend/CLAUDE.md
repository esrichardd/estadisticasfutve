# Backend — Convenciones de código

## Stack

Python 3.13 · FastAPI · SQLAlchemy 2.0 async · Pydantic v2 · Alembic · uv

---

## Schemas (Pydantic v2)

Tres clases por entidad, siempre con estos sufijos:

```python
class TeamCreate(TeamBase):   # campos requeridos para crear
class TeamUpdate(TeamBase):   # todos Optional, para PATCH semántico
class TeamResponse(TeamBase): # lo que sale por la API
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

- `TeamUpdate` usa `model_dump(exclude_none=True)` en el endpoint para no pisar campos no enviados.
- Campos calculados al vuelo (ej. `age` en `PlayerResponse`) se definen con `@computed_field`.
- `StandingResponse` no tiene `Create`/`Update` — los standings se calculan, no se crean directamente.

## Repositories

Funciones `async def`, no clases. El primer argumento siempre es `session: AsyncSession`.

```python
# ✅ correcto
async def get_all(session: AsyncSession, *, only_active: bool = False) -> list[Team]:
    ...

# ❌ incorrecto — no usar clases
class TeamRepository:
    ...
```

- `repositories/base.py` tiene las operaciones genéricas (`get_by_id`, `get_all`, `create`, `update`, `delete`). Usarlas cuando no hay lógica específica.
- Los repos no llaman a otros repos ni a services.
- Queries con filtros opcionales: construir el `select()` base y agregar `.where()` condicionalmente.

## Routers

- No tienen lógica de negocio. Llaman a `*_repo` (operaciones simples) o a `services/` (lógica).
- `404` explícito cuando `get_by_id` devuelve `None`.
- `POST` devuelve `status_code=201`.
- `PATCH` usa semántica parcial: `data.model_dump(exclude_none=True)`.

```python
@router.patch("/{team_id}", response_model=TeamResponse)
async def update_team(team_id: UUID, data: TeamUpdate, db: AsyncSession = Depends(get_db)):
    team = await team_repo.get_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return await team_repo.update(db, team, data.model_dump(exclude_none=True))
```

## Modelos SQLAlchemy

- Todos los modelos heredan de `Base` y `TimestampMixin` (de `app.models.base`).
- PKs son `UUID` con `default=uuid.uuid4`.
- Enums compartidos viven en `app/models/enums.py` como `class X(str, enum.Enum)`.
- Al crear un modelo nuevo, agregarlo al `__init__.py` de `models/` con `# noqa: F401` para que Alembic lo detecte.

## Seguridad

- Todos los endpoints bajo `/api/v1/*` están protegidos con `x-api-key` automáticamente (aplicado en `router.py`).
- No agregar la dependencia endpoint por endpoint — ya está en el router principal.
- La dependencia vive en `app/dependencies/auth.py`.

## Config y variables de entorno

- Nunca usar `os.environ` directamente. Siempre importar `from app.config import settings`.
- Toda variable nueva se agrega a `Settings` en `config.py` y se documenta en `.env.example`.

## Reglas de dependencia entre capas

```
Router/View → Service → Repository → DB
```

- `Repository` nunca llama a otro `Repository` ni a un `Service`.
- `Service` nunca importa routers.
- `Model` nunca importa schemas ni routers.

## Convención de commits

`type(scope): description` — scopes: `backend`, `frontend`, `db`, `infra`, `docs`.
Ver `CONTRIBUTING.md` en la raíz.
