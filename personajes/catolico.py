"""
Maripili Cat�lica - Defensora de la moral y tradiciones
D�bil contra pol�ticos, fuerte contra segarros

Estad�sticas:
- Vida: 130
- Ataque: 20
- Defensa: 24
- Velocidad: 40
- Energ�a: 110
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
    Personaje: Maripili Cat�lica
    La t�pica se�ora de la parroquia que reza el rosario y juzga a todo el mundo.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Maripili de la Parroquia",
            tipo=" Cat�lica Conservadora",
            vida_base=130,
            ataque_base=20,
            defensa_base=24,
            velocidad_base=40,
            energia_base=110
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["politico", "moderno", "herejia"]
        self.fortalezas = ["religioso", "tradicional", "moral"]
        self.inmunidades = ["tentacion"]
        
        # Inicializar habilidades espec�ficas
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return "Defensora de la moral y tradiciones, d�bil contra pol�ticos"
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades �nicas de la Cat�lica."""
        self.habilidades = [
            RezarRosario(),
            AguaBendita(),
            SermonDominical(),
            MiradaJuzgadora(),
            ViernesSanto(),
            Excomulgar()
        ]
    
    def mostrar_stats(self):
        """Muestra estad�sticas con estilo cat�lico."""
        print(f"\n{C.NEGRITA}{C.MAGENTA} MARIPILI CAT�LICA {C.RESET}")
        super().mostrar_stats()