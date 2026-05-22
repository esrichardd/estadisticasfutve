# EstadisticasFutve

Plataforma para llevar seguimiento a los resultados actuales e históricos de la liga de fútbol venezolana.

---

## Stack

**Base de datos**
| | |
|---|---|
| Motor | PostgreSQL (latest) |
| Visualización | pgAdmin 4 |

**Backend**
| | |
|---|---|
| Framework | FastAPI (Python 3.13) |
| ORM | SQLAlchemy 2.0 async |
| Migraciones | Alembic |
| Package manager | uv |

**Frontend**
| | |
|---|---|
| Framework | Next.js 16.2.6 (App Router, TypeScript) |
| Estilos | Tailwind CSS v4 |
| Package manager | pnpm |

**Infraestructura:** Docker + Docker Compose

---

## Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- (Opcional, solo para desarrollo local sin Docker) Python 3.13+, Node.js 22+, pnpm

---

## Variables de entorno

Copiar el archivo de ejemplo y ajustar los valores:

```bash
cp .env.example .env
```

El `.env` incluido ya tiene valores listos para desarrollo local. **Nunca commitear `.env` a git.**

---

## Cómo correr el proyecto

```bash
docker compose up --build
```

Al iniciar, Docker:

1. Levanta PostgreSQL y espera a que esté healthy
2. Levanta pgAdmin con el servidor de Postgres pre-configurado
3. Corre las migraciones de Alembic automáticamente
4. Levanta FastAPI con hot reload
5. Levanta Next.js con hot reload

### URLs disponibles

| Servicio                    | URL                         |
| --------------------------- | --------------------------- |
| Frontend (Next.js)          | http://localhost:3000       |
| Backend (FastAPI)           | http://localhost:8000       |
| Documentación API (Swagger) | http://localhost:8000/docs  |
| Documentación API (ReDoc)   | http://localhost:8000/redoc |
| pgAdmin                     | http://localhost:5050       |

### Credenciales pgAdmin

Usar los valores definidos en `.env` (`PGADMIN_DEFAULT_EMAIL` y `PGADMIN_DEFAULT_PASSWORD`).

El servidor de PostgreSQL ya está pre-configurado. La password de la DB es el valor de `POSTGRES_PASSWORD` en `.env`.

---

## Hot Reload

Los cambios en el código se reflejan automáticamente sin reiniciar Docker:

- **Backend:** cualquier cambio en `backend/app/` → uvicorn recarga automáticamente
- **Frontend:** cualquier cambio en `frontend/app/` → Next.js recarga automáticamente
- **Migraciones:** los cambios en `backend/alembic/` también se sincronizan, pero para aplicar una nueva migración hay que correr el comando manualmente (ver abajo)

---

## Migraciones con Alembic

Las migraciones corren automáticamente al iniciar el contenedor del backend.

Para crear una nueva migración:

```bash
# Generar migración automática desde los modelos
docker compose exec backend uv run alembic revision --autogenerate -m "descripcion_del_cambio"

# Aplicar migraciones pendientes
docker compose exec backend uv run alembic upgrade head

# Ver historial de migraciones
docker compose exec backend uv run alembic history

# Revertir la última migración
docker compose exec backend uv run alembic downgrade -1
```

---

## Comandos útiles

```bash
# Ver logs de un servicio específico
docker compose logs -f backend
docker compose logs -f frontend

# Entrar a la shell del contenedor backend
docker compose exec backend bash

# Entrar a psql directamente
docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB

# Detener todo (preserva volúmenes)
docker compose down

# Detener y eliminar volúmenes (reset completo de la DB)
docker compose down -v
```
