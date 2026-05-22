# Guía de contribución — EstadisticasFutve

---

## Convención de commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/). El formato es:

```
<tipo>(<scope>): <descripción en imperativo, minúsculas>
```

### Tipos

| Tipo       | Cuándo usarlo                               |
| ---------- | ------------------------------------------- |
| `feat`     | Feature nueva                               |
| `fix`      | Corrección de bug                           |
| `docs`     | Solo documentación                          |
| `refactor` | Reorganización sin cambio de comportamiento |
| `perf`     | Optimización de rendimiento                 |
| `test`     | Agregar o corregir tests                    |
| `chore`    | Dependencias, configs, limpieza general     |

### Scopes

| Scope      | Qué cubre                                    |
| ---------- | -------------------------------------------- |
| `backend`  | Código Python en `backend/app/`              |
| `frontend` | Código TypeScript/Next.js en `frontend/`     |
| `db`       | Migraciones de Alembic en `backend/alembic/` |
| `infra`    | Docker, Docker Compose, variables de entorno |
| `docs`     | Documentación en `*/docs/` o archivos `.md`  |

### Ejemplos

```
feat(backend): implement standings recalculation service
feat(frontend): add tournament standings page
feat(db): add suspension_cycles table

fix(backend): correct goals_against calculation on own goals
fix(frontend): fix team logo not loading on mobile

docs(backend): add architecture overview
docs(db): add database schema reference

refactor(backend): extract match event logic into service layer

perf(backend): add index on match_events.match_id

chore(infra): upgrade postgres to 17
chore(backend): update fastapi to 0.115
```

### Reglas

- La descripción va en **minúsculas** y en **imperativo** ("add", "fix", "update" — no "added", "fixes", "updating").
- Sin punto al final.
- Máximo 72 caracteres en la primera línea.
- Si el cambio necesita más contexto, agrega un cuerpo separado por una línea en blanco.
