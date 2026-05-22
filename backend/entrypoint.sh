#!/bin/bash
set -e

echo "════════════════════════════════════════"
echo "  Corriendo migraciones con Alembic..."
echo "════════════════════════════════════════"
uv run alembic upgrade head

echo "════════════════════════════════════════"
echo "  Iniciando FastAPI con hot reload..."
echo "  http://localhost:8000"
echo "  http://localhost:8000/docs"
echo "════════════════════════════════════════"
exec uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
