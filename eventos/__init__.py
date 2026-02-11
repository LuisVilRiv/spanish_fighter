"""
Módulo de eventos aleatorios para Batalla Cómica Española.
Sistema de eventos WTF que ocurren durante el combate con probabilidades variables.
"""

from .eventos_aleatorios import (
    # Eventos normales
    JamonVolador,
    AbuelaAparece,
    OleImprovisado,
    BotellonSorpresa,
    TuristasDespistados,
    
    # Eventos raros
    SiestaRepentina,
    ConcursoDeTapas,
    LlamadaDeTelefono,
    QueTiempoMasRaro,
    
    # Eventos ultra raros
    FurgonetaBlanca,
    ConspiracionTortillera,
    PikachuFalso,
    EspirituDeLaFeria,
    MocoEnElDedo
)

# Clasificación por tipo
EVENTOS_NORMALES = [
    JamonVolador,
    AbuelaAparece,
    OleImprovisado,
    BotellonSorpresa,
    TuristasDespistados
]

EVENTOS_RAROS = [
    SiestaRepentina,
    ConcursoDeTapas,
    LlamadaDeTelefono,
    QueTiempoMasRaro
]

EVENTOS_ULTRA_RAROS = [
    FurgonetaBlanca,
    ConspiracionTortillera,
    PikachuFalso,
    EspirituDeLaFeria,
    MocoEnElDedo
]

# Todas las clases de eventos
TODOS_LOS_EVENTOS = EVENTOS_NORMALES + EVENTOS_RAROS + EVENTOS_ULTRA_RAROS

# Exportar todo
__all__ = [
    # Eventos normales
    'JamonVolador',
    'AbuelaAparece',
    'OleImprovisado',
    'BotellonSorpresa',
    'TuristasDespistados',
    
    # Eventos raros
    'SiestaRepentina',
    'ConcursoDeTapas',
    'LlamadaDeTelefono',
    'QueTiempoMasRaro',
    
    # Eventos ultra raros
    'FurgonetaBlanca',
    'ConspiracionTortillera',
    'PikachuFalso',
    'EspirituDeLaFeria',
    'MocoEnElDedo',
    
    # Clasificaciones
    'EVENTOS_NORMALES',
    'EVENTOS_RAROS',
    'EVENTOS_ULTRA_RAROS',
    'TODOS_LOS_EVENTOS'
]