"""
Mock temporal de leaders para la home.

TEMPORAL: este archivo se elimina cuando match_events esté poblada.
El endpoint GET /views/home/leaders pasará a calcular los datos desde
la tabla match_events filtrando por event_type IN ('goal', 'assist').

No contiene datos como si fueran oficiales — solo estructura vacía.
"""

from app.schemas.views.home import HomeLeadersResponse

LEADERS_MOCK: HomeLeadersResponse = HomeLeadersResponse(
    scorers=[],
    assisters=[],
)
