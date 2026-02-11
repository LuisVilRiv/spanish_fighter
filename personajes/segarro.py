"""
Amego Segarro - El personaje más español de todos
Especialista en pedir cosas y tener poca química con el jamón

Estadísticas:
- Vida: 85
- Ataque: 70
- Defensa: 40
- Velocidad: 65
- Energía: 100
"""

from .personaje_base import Personaje
from habilidades.habilidades_segarro import (
    DameCartera,
    PedirSigarrito,
    SuperMeca,
    CriticaConstructiva,
    ToPelma,
    PedirFavor
)
from utils import Colores as C

class Segarro(Personaje):
    """
    Personaje: Amego Segarro
    El típico colega que siempre te pide cosas y nunca devuelve el dinero.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Paco 'El Segarrito'",
            tipo="🎮 Amego Segarro",
            vida_base=85,
            ataque_base=70,
            defensa_base=40,
            velocidad_base=65,
            energia_base=100
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["religioso", "familiar", "autoridad"]
        self.fortalezas = ["verborrea", "callejero", "improvisacion"]
        self.inmunidades = ["deuda"]  # Los segarros son inmunes a las deudas
        
        # Inicializar habilidades específicas
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return "Especialista en pedir cosas y tener poca química con el jamón"
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas del Segarro."""
        self.habilidades = [
            DameCartera(),
            PedirSigarrito(),
            SuperMeca(),
            CriticaConstructiva(),
            ToPelma(),
            PedirFavor()
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo segarro."""
        print(f"\n{C.NEGRITA}{C.VERDE}┌───── AMEGO SEGARRO ─────┐{C.RESET}")
        super().mostrar_stats()