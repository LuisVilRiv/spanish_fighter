"""
Maripili Católica - Defensora de la moral y tradiciones
Débil contra políticos, fuerte contra segarros

Estadísticas:
- Vida: 75
- Ataque: 60
- Defensa: 70
- Velocidad: 55
- Energía: 110
"""

from .personaje_base import Personaje
from habilidades.habilidades_catolico import (
    RezarRosario,
    AguaBendita,
    SermonDominical,
    MiradaJuzgadora,
    ViernesSanto,
    Excomulgar
)
from utils import Colores as C

class Catolico(Personaje):
    """
    Personaje: Maripili Católica
    La típica señora de la parroquia que reza el rosario y juzga a todo el mundo.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Maripili de la Parroquia",
            tipo="📿 Católica Conservadora",
            vida_base=75,
            ataque_base=60,
            defensa_base=70,
            velocidad_base=55,
            energia_base=110
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["politico", "moderno", "herejia"]
        self.fortalezas = ["religioso", "tradicional", "moral"]
        self.inmunidades = ["tentacion"]
        
        # Inicializar habilidades específicas
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return "Defensora de la moral y tradiciones, débil contra políticos"
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas de la Católica."""
        self.habilidades = [
            RezarRosario(),
            AguaBendita(),
            SermonDominical(),
            MiradaJuzgadora(),
            ViernesSanto(),
            Excomulgar()
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo católico."""
        print(f"\n{C.NEGRITA}{C.MAGENTA}┌───── MARIPILI CATÓLICA ─────┐{C.RESET}")
        super().mostrar_stats()