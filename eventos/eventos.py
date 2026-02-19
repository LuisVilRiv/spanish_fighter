"""
eventos.py
Re-exporta las listas de eventos desde eventos_aleatorios.py.
Los sistemas de combate importan desde aquí.
"""
from eventos_aleatorios import (
    EventoBase,
    EVENTOS_NORMALES,
    EVENTOS_RAROS,
    EVENTOS_ULTRA_RAROS,
    TODOS_LOS_EVENTOS,
)

__all__ = [
    "EventoBase",
    "EVENTOS_NORMALES",
    "EVENTOS_RAROS",
    "EVENTOS_ULTRA_RAROS",
    "TODOS_LOS_EVENTOS",
]