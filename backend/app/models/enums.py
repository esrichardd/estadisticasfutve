import enum


class PhaseType(str, enum.Enum):
    """Tipo de fase dentro de un torneo."""

    round_robin = "round_robin"  # Todos contra todos (liga clásica)
    group_stage = "group_stage"  # Fase de grupos (varios round-robins en paralelo)
    knockout = "knockout"        # Eliminación directa (un solo partido)
    two_legged = "two_legged"    # Eliminación directa con ida y vuelta


class MatchStatus(str, enum.Enum):
    """Estado de un partido."""

    scheduled = "scheduled"   # Programado
    live = "live"             # En juego
    finished = "finished"     # Finalizado
    postponed = "postponed"   # Postergado
    cancelled = "cancelled"   # Cancelado


class RefereeRole(str, enum.Enum):
    """Rol de un árbitro en un partido."""

    main = "main"
    assistant_1 = "assistant_1"
    assistant_2 = "assistant_2"
    fourth_official = "fourth_official"
    var = "var"


class EventType(str, enum.Enum):
    """Tipo de evento registrado en un partido."""

    goal = "goal"                         # Gol
    own_goal = "own_goal"                 # Autogol
    assist = "assist"                     # Asistencia
    yellow_card = "yellow_card"           # Tarjeta amarilla
    second_yellow = "second_yellow"       # Segunda amarilla (implica expulsión)
    red_card = "red_card"                 # Roja directa
    substitution_in = "substitution_in"   # Jugador que entra
    substitution_out = "substitution_out" # Jugador que sale
    penalty_miss = "penalty_miss"         # Penalti fallado
    penalty_saved = "penalty_saved"       # Penalti atajado


class ScopeType(str, enum.Enum):
    """Ámbito de un ciclo de apercibido."""

    tournament = "tournament"  # El ciclo aplica a todo el torneo
    phase = "phase"            # El ciclo se reinicia por fase
