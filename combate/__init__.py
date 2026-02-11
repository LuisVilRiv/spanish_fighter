"""
Módulo de combate para Batalla Cómica Española.
Sistema de combate por turnos con eventos aleatorios y personajes surrealistas.
"""

from .sistema_combate import (
    Combate,
    EstadoCombate,
    Accion,
    ResultadoTurno,
    ResultadoCombate
)

__all__ = [
    'Combate',
    'EstadoCombate',
    'Accion',
    'ResultadoTurno',
    'ResultadoCombate'
]