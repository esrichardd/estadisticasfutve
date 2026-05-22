# Arquitectura del Backend — EstadisticasFutve

Guía de referencia para entender cómo está organizado el backend, qué hace cada capa, y cómo fluye la información desde la base de datos hasta el frontend.

---

## Índice

- [Principio central](#principio-central)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Flujo de una petición](#flujo-de-una-petición)
- [Capas](#capas)
  - [main.py — Punto de entrada](#mainpy--punto-de-entrada)
  - [config.py — Configuración](#configpy--configuración)
  - [database.py — Conexión a la DB](#databasepy--conexión-a-la-db)
  - [models/ — Tablas de la DB](#models--tablas-de-la-db)
  - [schemas/ — Contratos de la API](#schemas--contratos-de-la-api)
  - [repositories/ — Queries a la DB](#repositories--queries-a-la-db)
  - [services/ — Lógica de negocio](#services--lógica-de-negocio)
  - [api/v1/ — Endpoints base](#apiv1--endpoints-base)
  - [api/v1/views/ — Endpoints por pantalla](#apiv1views--endpoints-por-pantalla)
  - [jobs/ — CRONs y scrapers](#jobs--crons-y-scrapers)
- [Reglas de dependencia entre capas](#reglas-de-dependencia-entre-capas)

---

## Principio central

Cada capa tiene **una única responsabilidad**. Ninguna capa hace el trabajo de otra.

```
HTTP Request
     ↓
  Router          ← recibe la petición, valida params, devuelve respuesta
     ↓
  Service         ← aplica lógica de negocio, orquesta repositorios
     ↓
  Repository      ← ejecuta queries contra la DB, nada más
     ↓
  PostgreSQL
```

Esto hace que el código sea fácil de leer, modificar y testear. Si el día de mañana cambia cómo se calculan los standings, solo tocas `standings_service.py`. Si cambia una query, solo tocas `standing_repo.py`. Nunca los dos a la vez.

---

## Estructura de carpetas

```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── base.py
│   │   ├── league.py
│   │   ├── season.py
│   │   ├── team.py
│   │   ├── player.py
│   │   ├── match.py
│   │   ├── match_event.py
│   │   ├── standing.py
│   │   └── suspension.py
│   │
│   ├── schemas/
│   │   ├── league.py
│   │   ├── team.py
│   │   ├── player.py
│   │   ├── match.py
│   │   ├── standing.py
│   │   └── views/
│   │       ├── match_view.py
│   │       ├── tournament_view.py
│   │       └── player_view.py
│   │
│   ├── repositories/
│   │   ├── base.py
│   │   ├── league_repo.py
│   │   ├── team_repo.py
│   │   ├── player_repo.py
│   │   ├── match_repo.py
│   │   ├── standing_repo.py
│   │   └── stats_repo.py
│   │
│   ├── services/
│   │   ├── stats_service.py
│   │   ├── standings_service.py
│   │   └── suspension_service.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       ├── leagues.py
│   │       ├── seasons.py
│   │       ├── teams.py
│   │       ├── players.py
│   │       ├── matches.py
│   │       ├── standings.py
│   │       └── views/
│   │           ├── match_view.py
│   │           ├── tournament_view.py
│   │           └── player_view.py
│   │
│   └── jobs/
│       ├── scheduler.py
│       └── scrapers/
│           ├── base_scraper.py
│           └── futve_scraper.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
└── docs/
    ├── architecture/
    │   └── README.md          ← este archivo
    └── database/
        └── README.md
```

---

## Flujo de una petición

Para entender cómo encajan las capas, este es el recorrido completo de una petición real:

> **"Dame la tabla de posiciones del Apertura 2025, Grupo A"**

```
GET /api/v1/views/tournament/3/standings

1. api/v1/views/tournament_view.py
   → recibe phase_id=3, group_id=1 de los query params
   → llama a standings_service.get_standings(phase_id=3, group_id=1)

2. services/standings_service.py
   → sabe que tiene que devolver standings con info de equipo enriquecida
   → llama a standing_repo.fetch_by_phase_and_group(phase_id=3, group_id=1)
   → combina con team_repo.fetch_by_ids([...]) para agregar logos y nombres

3. repositories/standing_repo.py
   → ejecuta el SELECT contra PostgreSQL
   → devuelve los registros crudos de la DB

4. De vuelta en el router
   → serializa el resultado con el schema StandingsViewResponse
   → FastAPI devuelve el JSON al frontend
```

El frontend hizo **una sola llamada** y recibió todo lo que necesita para pintar la pantalla.

---

## Capas

---

### `main.py` — Punto de entrada

Es donde vive la aplicación FastAPI. Su trabajo es arrancar la app, registrar todos los routers y configurar los eventos de inicio (como conectar el scheduler de CRONs).

No tiene lógica de negocio. Es solo el "pegamento" que une todo.

```
Responsabilidad: crear la app, registrar routers, manejar startup/shutdown
```

---

### `config.py` — Configuración

Lee las variables de entorno del archivo `.env` usando Pydantic Settings. Así en el resto del código nunca escribes `os.environ["DATABASE_URL"]` directamente; en cambio, importas `settings.database_url`.

Si mañana cambias cómo se llama una variable de entorno, solo lo cambias aquí.

```
Responsabilidad: centralizar y tipar todas las variables de configuración
```

---

### `database.py` — Conexión a la DB

Configura el engine async de SQLAlchemy y la fábrica de sesiones. Exporta una función `get_session` que los routers usan como dependencia inyectada.

Cada petición HTTP recibe su propia sesión de DB que se abre al entrar y se cierra al salir, sin importar si hubo error o no.

```
Responsabilidad: gestionar el ciclo de vida de las conexiones a PostgreSQL
```

---

### `models/` — Tablas de la DB

Son las clases Python que representan las tablas de PostgreSQL. SQLAlchemy las usa para construir queries y mapear resultados a objetos.

Cada archivo corresponde a una (o varias tablas relacionadas). Por ejemplo, `match.py` define los modelos `Match` y `MatchOfficial`.

**Importante:** los modelos son el espejo de la DB. No tienen lógica de negocio. No saben nada de la API.

```
Responsabilidad: describir la estructura de las tablas para SQLAlchemy
Ejemplo: models/match.py → tabla `matches`, tabla `match_officials`
```

---

### `schemas/` — Contratos de la API

Son clases Pydantic que describen la forma de los datos que entran y salen de la API. FastAPI los usa para validar automáticamente lo que llega y serializar lo que sale.

La separación con `models/` es intencional y crítica:

|                               | `models/`               | `schemas/`           |
| ----------------------------- | ----------------------- | -------------------- |
| Qué describe                  | Cómo se guarda en la DB | Cómo se ve en la API |
| Lo usa                        | SQLAlchemy              | FastAPI + Pydantic   |
| Puede tener campos calculados | No                      | Sí                   |
| Expone todo lo de la DB       | Sí                      | Solo lo necesario    |

Por ejemplo, `players` en la DB tiene `birth_date`. El schema de respuesta puede exponer además `age` calculada al vuelo, sin que exista ese campo en la tabla.

La subcarpeta `schemas/views/` tiene schemas compuestos — los que agrupan datos de varias tablas para responder una pantalla completa.

```
Responsabilidad: definir qué datos entran y salen de cada endpoint
```

---

### `repositories/` — Queries a la DB

Aquí viven todas las queries SQL (escritas con SQLAlchemy). Son funciones simples que reciben parámetros, hablan con la DB, y devuelven resultados. Sin lógica de negocio.

La idea es que si mañana quieres cambiar una query (agregar un índice, optimizar un JOIN), sabes exactamente dónde ir.

`base.py` tiene un repositorio genérico con operaciones comunes (get by id, list, create, update, delete) que los demás repositorios heredan o reutilizan.

`stats_repo.py` merece mención especial: tiene las queries de agregación más complejas, como "top goleadores de un torneo" o "tarjetas por árbitro", que implican `GROUP BY`, `JOIN` a varias tablas, etc.

```
Responsabilidad: ejecutar queries contra PostgreSQL, devolver datos crudos
Regla: ningún repositorio llama a otro repositorio ni a un service
```

---

### `services/` — Lógica de negocio

Es la capa más importante del backend. Aquí vive todo lo que no es ni una query ni un endpoint: los cálculos, las reglas de negocio, las decisiones.

Los tres servicios principales de este dominio:

**`stats_service.py`**
Calcula estadísticas derivadas de `match_events`. Goleadores, asistidores, tarjetas, minutos jugados. Recibe un `tournament_id` o `phase_id` y devuelve los datos ya procesados.

**`standings_service.py`**
Recalcula la tabla de posiciones al finalizar un partido. Lee los eventos del partido terminado, actualiza los campos de la tabla `standings` (puntos, goles, partidos jugados). Es el servicio que se llama desde el job de actualización automática.

**`suspension_service.py`**
Gestiona el sistema de apercibidos. Cuando se registra una tarjeta amarilla, verifica `suspension_cycles`, incrementa el contador, y si llega al `threshold`, marca al jugador como suspendido. También maneja el reinicio del ciclo cuando `cards_reset_on_start` está activo en una fase.

```
Responsabilidad: lógica de negocio, cálculos, reglas del dominio
Regla: un service puede llamar a repositorios y a otros services, nunca a routers
```

---

### `api/v1/` — Endpoints base

Los routers de FastAPI organizados por recurso. Cada archivo expone las operaciones estándar sobre una entidad:

| Archivo        | Endpoints típicos                                    |
| -------------- | ---------------------------------------------------- |
| `leagues.py`   | GET /leagues, GET /leagues/{id}                      |
| `teams.py`     | GET /teams, GET /teams/{id}                          |
| `matches.py`   | GET /matches, GET /matches/{id}, PATCH /matches/{id} |
| `players.py`   | GET /players, GET /players/{id}                      |
| `standings.py` | GET /standings?phase_id=X                            |

Estos endpoints son simples y de propósito general. Son útiles para el panel de administración, para poblar dropdowns, o para cualquier consulta que no necesite datos combinados de varias tablas.

`router.py` es el archivo que agrupa todos los sub-routers y los registra bajo el prefijo `/api/v1`.

```
Responsabilidad: recibir peticiones HTTP, llamar al service correcto, devolver respuesta
Regla: un router no hace queries directamente ni tiene lógica de negocio
```

---

### `api/v1/views/` — Endpoints por pantalla

Son endpoints diseñados para responder exactamente lo que necesita una pantalla del frontend, en una sola llamada. No hay lógica nueva aquí: solo llaman a los services ya existentes y combinan sus resultados en un schema de respuesta compuesta.

Las vistas más importantes para este dominio:

**`match_view.py`** → `GET /views/matches/{id}`
Devuelve en una sola respuesta: datos del partido, eventos con minuto y jugador, árbitros, y si aplica el marcador global de la eliminatoria (`tie_id`).

**`tournament_view.py`** → `GET /views/tournaments/{id}`
Devuelve: resumen del torneo, sus fases, la tabla de posiciones de cada fase/grupo, y los últimos resultados.

**`player_view.py`** → `GET /views/players/{id}`
Devuelve: datos del jugador, su historial de equipos, estadísticas acumuladas (goles, asistencias, tarjetas) y su estado de suspensión actual.

Si el frontend necesita una pantalla nueva con datos que no encajan en ninguna vista existente, se crea un nuevo archivo aquí. No se modifica ninguna otra capa.

```
Responsabilidad: componer respuestas orientadas a pantallas específicas del frontend
Regla: una vista no tiene lógica propia, solo orquesta services
```

---

### `jobs/` — CRONs y scrapers

Las tareas programadas que alimentan la DB automáticamente.

**`scheduler.py`**
Configura APScheduler, la librería que maneja los CRONs dentro del proceso de FastAPI. Define qué función corre y con qué frecuencia (por ejemplo, "cada noche a las 2am, actualizar resultados del día").

**`scrapers/base_scraper.py`**
Clase base con utilidades comunes: manejo de errores de red, reintentos, logging. Todos los scrapers específicos la heredan.

**`scrapers/futve_scraper.py`**
El scraper concreto para obtener datos de la liga venezolana. Va a buscar resultados a la fuente externa, transforma los datos al formato de la DB, y los persiste usando los mismos repositorios que usa el resto de la app. No tiene acceso directo a la DB; pasa siempre por los repositorios.

```
Responsabilidad: obtener datos externos y persistirlos en la DB
Regla: los scrapers usan repositorios para escribir en la DB, no SQL directo
```

---

## Reglas de dependencia entre capas

Para que la arquitectura se mantenga ordenada a medida que crece el proyecto:

```
✅ Router      → puede llamar a Service
✅ Router      → puede llamar a Repository (solo en casos simples, sin lógica)
✅ Service     → puede llamar a Repository
✅ Service     → puede llamar a otro Service
✅ Scraper     → puede llamar a Repository
✅ View Router → puede llamar a Service

❌ Repository  → nunca llama a Service ni a otro Repository
❌ Repository  → nunca tiene lógica de negocio
❌ Model       → nunca importa schemas ni routers
❌ Service     → nunca importa routers
```

La regla de oro: las dependencias solo van hacia abajo en la jerarquía. Nunca hacia arriba.

```
Router / View
     ↓
  Service
     ↓
  Repository
     ↓
  PostgreSQL
```
