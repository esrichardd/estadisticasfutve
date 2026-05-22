"""Crear esquema de base de datos de fútbol

Crea las 17 tablas del dominio en orden de dependencia de FK:
  1. Entidades independientes : leagues, teams, players, referees
  2. Nivel temporada          : seasons, season_teams, player_registrations
  3. Estructura del torneo    : tournaments, tournament_phases, phase_groups, group_teams
  4. Partidos                 : rounds, matches, match_officials, match_events
  5. Derivadas                : standings, suspension_cycles

Tipos ENUM de PostgreSQL creados:
  - phase_type_enum    : round_robin | group_stage | knockout | two_legged
  - match_status_enum  : scheduled | live | finished | postponed | cancelled
  - referee_role_enum  : main | assistant_1 | assistant_2 | fourth_official | var
  - event_type_enum    : goal | own_goal | assist | yellow_card | second_yellow |
                         red_card | substitution_in | substitution_out |
                         penalty_miss | penalty_saved
  - scope_type_enum    : tournament | phase

Revision ID: 002
Revises: 001
Create Date: 2026-05-21
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ── 1. Entidades independientes (sin FK entre sí) ─────────────────────────

    op.create_table(
        "leagues",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("federation", sa.String(100), nullable=True),
        sa.Column("logo_url", sa.String(500), nullable=True),
        sa.Column("website", sa.String(500), nullable=True),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")
        ),
    )

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("short_name", sa.String(100), nullable=True),
        sa.Column("abbreviation", sa.String(3), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("stadium", sa.String(200), nullable=True),
        sa.Column("logo_url", sa.String(500), nullable=True),
        sa.Column("founded_year", sa.Integer(), nullable=True),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")
        ),
    )

    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("nationality", sa.String(100), nullable=True),
        sa.Column("position", sa.String(50), nullable=True),
    )

    op.create_table(
        "referees",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("nationality", sa.String(100), nullable=True),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")
        ),
    )

    # ── 2. Nivel Temporada ────────────────────────────────────────────────────

    op.create_table(
        "seasons",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "league_id",
            sa.Integer(),
            sa.ForeignKey("leagues.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("display_name", sa.String(20), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
    )

    op.create_table(
        "season_teams",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "season_id",
            sa.Integer(),
            sa.ForeignKey("seasons.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.UniqueConstraint("season_id", "team_id", name="uq_season_team"),
    )

    op.create_table(
        "player_registrations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "player_id",
            sa.Integer(),
            sa.ForeignKey("players.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "season_id",
            sa.Integer(),
            sa.ForeignKey("seasons.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("jersey_number", sa.Integer(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),  # NULL = aún activo
        sa.Column(
            "is_loan", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column("notes", sa.Text(), nullable=True),
    )

    # ── 3. Estructura del Torneo ──────────────────────────────────────────────

    op.create_table(
        "tournaments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "season_id",
            sa.Integer(),
            sa.ForeignKey("seasons.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(100), nullable=False),
        # 'order' es palabra reservada en SQL; SQLAlchemy lo entrecomilla automáticamente
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
    )

    op.create_table(
        "tournament_phases",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "tournament_id",
            sa.Integer(),
            sa.ForeignKey("tournaments.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column(
            "phase_type",
            sa.Enum(
                "round_robin",
                "group_stage",
                "knockout",
                "two_legged",
                name="phase_type_enum",
            ),
            nullable=False,
        ),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column(
            "num_legs", sa.Integer(), nullable=False, server_default=sa.text("1")
        ),
        sa.Column("promotion_spots", sa.Integer(), nullable=True),
        sa.Column(
            "cards_reset_on_start",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.create_table(
        "phase_groups",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "phase_id",
            sa.Integer(),
            sa.ForeignKey("tournament_phases.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(100), nullable=False),
    )

    op.create_table(
        "group_teams",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "group_id",
            sa.Integer(),
            sa.ForeignKey("phase_groups.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("seed", sa.Integer(), nullable=True),
    )

    # ── 4. Partidos ───────────────────────────────────────────────────────────

    op.create_table(
        "rounds",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "phase_id",
            sa.Integer(),
            sa.ForeignKey("tournament_phases.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "group_id",
            sa.Integer(),
            sa.ForeignKey("phase_groups.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("date_start", sa.Date(), nullable=True),
        sa.Column("date_end", sa.Date(), nullable=True),
    )

    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "round_id",
            sa.Integer(),
            sa.ForeignKey("rounds.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "home_team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "away_team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        # tie_id agrupa los dos partidos de una eliminatoria de ida y vuelta
        sa.Column("tie_id", sa.Integer(), nullable=True),
        sa.Column("leg", sa.Integer(), nullable=True),  # 1=ida, 2=vuelta
        # FK autorreferencial: apunta al partido del Apertura del que
        # este (Clausura) es la vuelta con localía invertida
        sa.Column(
            "reverse_of_match_id",
            sa.Integer(),
            sa.ForeignKey("matches.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("scheduled_datetime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("venue", sa.String(200), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "scheduled",
                "live",
                "finished",
                "postponed",
                "cancelled",
                name="match_status_enum",
            ),
            nullable=False,
            server_default=sa.text("'scheduled'"),
        ),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
    )

    op.create_table(
        "match_officials",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "match_id",
            sa.Integer(),
            sa.ForeignKey("matches.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "referee_id",
            sa.Integer(),
            sa.ForeignKey("referees.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "role",
            sa.Enum(
                "main",
                "assistant_1",
                "assistant_2",
                "fourth_official",
                "var",
                name="referee_role_enum",
            ),
            nullable=False,
        ),
    )

    op.create_table(
        "match_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "match_id",
            sa.Integer(),
            sa.ForeignKey("matches.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "player_id",
            sa.Integer(),
            sa.ForeignKey("players.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        # team_id SIEMPRE explícito: nunca derivado de player_registrations
        sa.Column(
            "team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "event_type",
            sa.Enum(
                "goal",
                "own_goal",
                "assist",
                "yellow_card",
                "second_yellow",
                "red_card",
                "substitution_in",
                "substitution_out",
                "penalty_miss",
                "penalty_saved",
                name="event_type_enum",
            ),
            nullable=False,
        ),
        sa.Column("minute", sa.Integer(), nullable=False),
        sa.Column("added_time", sa.Integer(), nullable=True),
        # Jugador secundario: el asistidor en un gol, o quién entra/sale en sustitución
        sa.Column(
            "related_player_id",
            sa.Integer(),
            sa.ForeignKey("players.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )

    # ── 5. Derivadas ──────────────────────────────────────────────────────────

    op.create_table(
        "standings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "phase_id",
            sa.Integer(),
            sa.ForeignKey("tournament_phases.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "group_id",
            sa.Integer(),
            sa.ForeignKey("phase_groups.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column(
            "team_id",
            sa.Integer(),
            sa.ForeignKey("teams.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("played", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("won", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("drawn", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("lost", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column(
            "goals_for", sa.Integer(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "goals_against", sa.Integer(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "goal_difference",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "points", sa.Integer(), nullable=False, server_default=sa.text("0")
        ),
        sa.Column(
            "last_updated",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("phase_id", "group_id", "team_id", name="uq_standing"),
    )

    op.create_table(
        "suspension_cycles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "player_id",
            sa.Integer(),
            sa.ForeignKey("players.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "scope_type",
            sa.Enum("tournament", "phase", name="scope_type_enum"),
            nullable=False,
        ),
        # scope_id apunta a tournament.id o tournament_phases.id según scope_type
        sa.Column("scope_id", sa.Integer(), nullable=False),
        sa.Column(
            "yellow_count_in_cycle",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "threshold", sa.Integer(), nullable=False, server_default=sa.text("4")
        ),
        sa.Column(
            "is_suspended",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "suspension_served",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "cycle_number", sa.Integer(), nullable=False, server_default=sa.text("1")
        ),
    )


def downgrade() -> None:
    # Eliminar tablas en orden inverso a sus dependencias de FK

    # 5. Derivadas
    op.drop_table("suspension_cycles")
    op.drop_table("standings")

    # 4. Partidos
    op.drop_table("match_events")
    op.drop_table("match_officials")
    op.drop_table("matches")
    op.drop_table("rounds")

    # 3. Estructura del torneo
    op.drop_table("group_teams")
    op.drop_table("phase_groups")
    op.drop_table("tournament_phases")
    op.drop_table("tournaments")

    # 2. Nivel temporada
    op.drop_table("player_registrations")
    op.drop_table("season_teams")
    op.drop_table("seasons")

    # 1. Entidades independientes
    op.drop_table("referees")
    op.drop_table("players")
    op.drop_table("teams")
    op.drop_table("leagues")

    # Eliminar tipos ENUM de PostgreSQL (en orden inverso de creación)
    op.execute("DROP TYPE IF EXISTS scope_type_enum")
    op.execute("DROP TYPE IF EXISTS event_type_enum")
    op.execute("DROP TYPE IF EXISTS referee_role_enum")
    op.execute("DROP TYPE IF EXISTS match_status_enum")
    op.execute("DROP TYPE IF EXISTS phase_type_enum")
