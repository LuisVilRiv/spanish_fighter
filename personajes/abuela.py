"""
Abuela Española - Tu abuela, la de todos. Te da de comer y te riñe.
Poder absoluto sobre la familia y la cocina

Estadísticas:
- Vida: 110
- Ataque: 22
- Defensa: 14
- Velocidad: 50
- Energía: 90
"""

from .personaje_base import Personaje
from habilidades.habilidades_abuela import (
    CucharonDeMadera,
    ComeHijo,
    ChismeVenenoso,
    RemedioCasero,
    MiradaQueMata,
    BufandaDeLana
)
from utils import Colores as C
import random

class Abuela(Personaje):
    """
    Personaje: Abuela Española
    Tu abuela, la de todos. Te da de comer y te riñe.
    Poder absoluto sobre la familia y la cocina.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Doña Remedios",
            tipo="� Abuela Española",
            vida_base=110,
            ataque_base=22,
            defensa_base=14,
            velocidad_base=50,
            energia_base=90
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["moderno", "tecnologia", "desobediencia"]
        self.fortalezas = ["tradicional", "familiar", "cocina", "sabiduria"]
        self.inmunidades = ["chantaje", "mentira"]  # Las abuelas lo saben todo
        
        # Estadísticas especiales de la abuela
        self._comidas_preparadas = 0
        self._capones_dados = 0
        self._consejos_dados = 0
        self._remedios_aplicados = 0
        self._autoridad = 100  # Autoridad sobre la familia
        
        # Frases típicas de abuela
        self._frases_abuela = [
            "¡Ay, que te vas a matar, chaval!",
            "¡Come, hijo, que estás en los huesos!",
            "En mis tiempos esto no pasaba",
            "¡Por la señal de la santa cruz!",
            "¡Que Dios te oiga!",
            "¡A mí no me mires con esa cara!",
            "¡Esto es cosa del demonio!",
            "¡Te voy a dar un capón!"
        ]
        
        # Recetas de cocina
        self._recetas = [
            "cocido madrileño",
            "paella",
            "tortilla de patatas",
            "potaje",
            "lentejas",
            "croquetas",
            "flan",
            "natillas"
        ]
        
        # Inicializar habilidades
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("Tu abuela, la de todos. Te da de comer y te riñe. "
                "Poder absoluto sobre la familia y la cocina. "
                "Nadie se atreve a desobedecerla.")
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas de la Abuela."""
        self.habilidades = [
            CucharonDeMadera(),   # Habilidad 1: Golpe con cucharón
            ComeHijo(),           # Habilidad 2: Te obliga a comer
            ChismeVenenoso(),     # Habilidad 3: Chisme que duele
            RemedioCasero(),      # Habilidad 4: Remedio mágico
            MiradaQueMata(),      # Habilidad 5: Mirada paralizante
            BufandaDeLana()       # Habilidad 6: Te abriga
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo abuela."""
        print(f"\n{C.NEGRITA}{C.MAGENTA}������ ABUELA ESPA�OLA ������{C.RESET}")
        super().mostrar_stats()
        
        # Mostrar estadísticas especiales
        print(f"\n{C.AMARILLO}������ ESTADÍSTICAS MATRIARCALES ������{C.RESET}")
        print(f"{C.CYAN}� Comidas preparadas: {self._comidas_preparadas:3}        �{C.RESET}")
        print(f"{C.CYAN}� Capones dados: {self._capones_dados:3}             �{C.RESET}")
        print(f"{C.CYAN}� Consejos dados: {self._consejos_dados:3}            �{C.RESET}")
        print(f"{C.CYAN}� Remedios aplicados: {self._remedios_aplicados:3}        �{C.RESET}")
        print(f"{C.CYAN}� Autoridad: {self._autoridad:3}                �{C.RESET}")
        print(f"{C.AMARILLO}����������������������������������������{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """Recibir daño con modificadores especiales para Abuela."""
        # Las abuelas son duras como roble (reducción por edad)
        reduccion_edad = dano // 4
        dano = max(1, dano - reduccion_edad)
        
        # Vulnerable a lo moderno
        if tipo_dano in ["tecnologia", "moderno", "internet"]:
            dano = int(dano * 1.6)
            print(f"{C.ROJO}¡No entiende estas modernidades! +60% daño{C.RESET}")
        
        # Inmune a las mentiras
        if tipo_dano == "mentira":
            print(f"{C.AZUL}¡Las abuelas huelen la mentira! Inmune.{C.RESET}")
            return 0
        
        # Aumenta autoridad cuando le atacan
        self._autoridad = min(150, self._autoridad + 5)
        
        return super().recibir_dano(dano, tipo_dano, critico)
    
    def regenerar(self):
        """Regeneración de la abuela."""
        super().regenerar()
        
        # La abuela siempre está cocinando (25%)
        if random.random() < 0.25:
            receta = random.choice(self._recetas)
            self._comidas_preparadas += 1
            
            # La comida cura
            curacion = random.randint(5, 15)
            self.vida_actual = min(self.vida_maxima, self.vida_actual + curacion)
            
            print(f"{C.VERDE}¡Prepara {receta}! Se cura {curacion} puntos. Total: {self._comidas_preparadas} comidas.{C.RESET}")
        
        # Da consejos (30%)
        if random.random() < 0.3:
            self._consejos_dados += 1
            consejos = [
                "ponte un chaquetón",
                "no salgas con el pelo mojado",
                "come más legumbres",
                "llama a tu madre",
                "reza un avemaría"
            ]
            consejo = random.choice(consejos)
            print(f"{C.CYAN}» {self.nombre}: \"{consejo}\". Consejos: {self._consejos_dados}{C.RESET}")
    
    def dar_capon(self):
        """Da un capón (golpe cariñoso)."""
        self._capones_dados += 1
        print(f"{C.ROJO}¡Te voy a dar un capón! Total: {self._capones_dados}{C.RESET}")
        
        # Aumenta autoridad
        self._autoridad = min(150, self._autoridad + 10)
    
    def aplicar_remedio(self):
        """Aplica un remedio casero."""
        self._remedios_aplicados += 1
        remedios = [
            "vicks vaporub",
            "agua con limón",
            "infusión de manzanilla",
            "ajo en la almohada",
            "pañuelo con alcanfor"
        ]
        remedio = random.choice(remedios)
        print(f"{C.MAGENTA}¡Aplica {remedio}! Remedios: {self._remedios_aplicados}{C.RESET}")
        
        return remedio