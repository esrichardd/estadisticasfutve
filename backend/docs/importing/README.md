# Poblamiento de datos

Esta guia documenta como poblar la base de datos de EstadisticasFutve de forma
incremental, repetible e idempotente. La regla central es cargar primero la
estructura deportiva y dejar los datos granulares para fases posteriores.

## Estrategia en cuatro fases

1. **Seed estructural**
   - Carga `leagues`, `seasons`, `teams`, `season_teams`, `tournaments`,
     `tournament_phases`, `phase_groups` y `group_teams`.
   - No crea partidos, jugadores, eventos, standings ni suspensiones.
   - Archivo actual:
     `backend/data/seeds/futve_2026_apertura_structure.json`.

2. **Fixture**
   - Crea `rounds` y `matches` desde calendario oficial o fuente normalizada.
   - Debe ejecutarse despues del seed estructural.
   - Cada partido debe referenciar equipos ya inscritos en la temporada.

3. **Resultados**
   - Actualiza `matches.status`, `matches.home_score` y `matches.away_score`.
   - Al finalizar esta fase, `standings` debe recalcularse desde partidos
     finalizados, no cargarse manualmente como verdad primaria.

4. **Eventos**
   - Carga `players`, `player_registrations`, `referees`, `match_officials` y
     `match_events`.
   - `match_events` es la fuente de verdad para estadisticas detalladas como
     goles, asistencias, tarjetas y sustituciones.
   - `suspension_cycles` debe recalcularse desde tarjetas y reglas de ciclo.

## Archivos permanentes y temporales

- `backend/app/jobs/importers/`: codigo permanente de importacion.
- `backend/scripts/`: comandos ejecutables para correr importadores.
- `backend/data/seeds/`: datasets pequenos y curados que pueden versionarse.
- `backend/data/raw/`: datos descargados o copiados de fuentes externas; no
  deberian versionarse por defecto.
- `backend/data/normalized/`: datos intermedios validados; versionarlos es una
  decision de trazabilidad.

## Seed Apertura 2026

El seed actual representa la estructura del Torneo Apertura 2026 de Liga FUTVE:

- Liga: Primera Division de Venezuela.
- Temporada: 2026.
- Torneo: Apertura.
- Fases:
  - Ronda Regular (`round_robin`), 13 fechas, 14 equipos.
  - Cuadrangulares (`group_stage`), dos grupos de cuatro equipos, ida y vuelta.
  - Final (`knockout`), partido unico.
- Equipos: 14 clubes participantes.

Grupos de Fase Final cargados:

- Cuadrangular A: Deportivo La Guaira, UCV FC, Portuguesa FC, Academia Puerto
  Cabello.
- Cuadrangular B: Metropolitanos FC, Deportivo Tachira, Estudiantes de Merida,
  Carabobo FC.

## Como ejecutar el seed

Desde `backend/`, con las variables de entorno configuradas:

```bash
python3 scripts/seed_structure.py
```

Tambien se puede pasar otro archivo:

```bash
python3 scripts/seed_structure.py --file data/seeds/otro_seed.json
```

El importador es idempotente: busca registros por claves naturales antes de
insertar. Correrlo dos veces no deberia duplicar la estructura.

## Claves naturales usadas

- Liga: `name + country`.
- Temporada: `league_id + display_name`.
- Equipo: `name`.
- Inscripcion de equipo: `season_id + team_id`.
- Torneo: `season_id + name`.
- Fase: `tournament_id + name`.
- Grupo: `phase_id + name`.
- Equipo en grupo: `group_id + team_id`.

## Fuentes consultadas

- Liga FUTVE, Fase Final Apertura 2026:
  https://ligafutve.org/la-fase-final-del-torneo-apertura-ya-definio-sus-enfrentamientos/
- Liga FUTVE, Clasificacion 2026:
  https://ligafutve.org/clasificacion-liga-futve/
- Liga FUTVE, Calendario 2026:
  https://ligafutve.org/calendario/
- La Vinotinto, calendario del Torneo Apertura 2026:
  https://www.lavinotinto.com/calendario-del-torneo-apertura-2026/
- Wikipedia, Torneo Apertura 2026 Venezuela, usada como apoyo secundario:
  https://es.wikipedia.org/wiki/Torneo_Apertura_2026_%28Venezuela%29

## Como continuar en otro chat o con otro LLM

1. Leer primero `backend/docs/database/README.md`.
2. Leer este documento.
3. Revisar el seed en `backend/data/seeds/futve_2026_apertura_structure.json`.
4. Mantener la carga por fases: estructura, fixture, resultados, eventos.
5. No cargar `standings` como fuente primaria; recalcularlo desde `matches`.
6. No derivar el equipo de un evento desde `player_registrations`; usar siempre
   el `team_id` explicito del evento.
