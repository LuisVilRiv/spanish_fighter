"""
Barrendero Filósofo - Barre las calles mientras piensa en el sentido de la vida
Sabio callejero con perspectiva única

Estadísticas:
- Vida: 105
- Ataque: 20
- Defensa: 15
- Velocidad: 55
- Energía: 95
"""

from .personaje_base import Personaje
from habilidades.habilidades_barrendero import (
    BarridoExistencial,
    FregonaDeLaVerdad,
    CuboDeLaSabiduria,
    MeditacionCallejera,
    FilosofiaDeBar,
    LimpiezaProfunda
)
from utils import Colores as C
import random

class Barrendero(Personaje):
    """
    Personaje: Barrendero Filósofo
    Barre las calles mientras piensa en el sentido de la vida.
    Sabio callejero con perspectiva única.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Don Limpio",
            tipo="� Barrendero Filósofo",
            vida_base=105,
            ataque_base=20,
            defensa_base=15,
            velocidad_base=55,
            energia_base=95
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["tecnologia", "automatizacion", "desprecio", "ignorancia"]
        self.fortalezas = ["reflexion", "paciencia", "sabiduria", "observacion"]
        self.inmunidades = ["suciedad", "tedio"]  # Está acostumbrado
        
        # Estadísticas especiales del barrendero
        self._calles_barridas = 0
        self._reflexiones_profundas = 0
        self._cosas_encontradas = 0
        self._consejos_dados = 0
        self._sabiduria = 100  # Nivel de sabiduría (0-100)
        
        # Frases filosóficas
        self._frases_filosoficas = [
            "Todo lo que sube, baja... como la basura",
            "La vida es como barrer: siempre hay más suciedad",
            "El sentido está en el camino, no en el destino",
            "Lo único constante es el cambio... y la suciedad",
            "Barro, luego existo",
            "La verdadera limpieza está dentro",
            "Cada basura tiene su historia",
            "El polvo del ayer es el recuerdo de hoy"
        ]
        
        # Cosas que encuentra
        self._hallazgos = [
            "una moneda antigua",
            "una carta de amor",
            "un juguete roto",
            "una llave misteriosa",
            "un diario abandonado",
            "una foto vieja",
            "un libro mojado",
            "un recuerdo perdido"
        ]
        
        # Reflexiones profundas
        self._reflexiones = [
            "sobre el paso del tiempo",
            "sobre la naturaleza humana",
            "sobre la sociedad de consumo",
            "sobre la fugacidad de la vida",
            "sobre el significado del trabajo",
            "sobre la belleza en lo simple",
            "sobre el ciclo de la vida",
            "sobre la conexión entre todo"
        ]
        
        # Inicializar habilidades
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("Barre las calles mientras piensa en el sentido de la vida. "
                "Sabio callejero con perspectiva única. "
                "Lento pero profundo, vulnerable al desprecio pero lleno de sabiduría.")
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas del Barrendero."""
        self.habilidades = [
            BarridoExistencial(),   # Habilidad 1: Barre y reflexiona
            FregonaDeLaVerdad(),    # Habilidad 2: Friega con sabiduría
            CuboDeLaSabiduria(),    # Habilidad 3: Lanza el cubo
            MeditacionCallejera(),  # Habilidad 4: Medita en la calle
            FilosofiaDeBar(),       # Habilidad 5: Filosofía de bar
            LimpiezaProfunda()      # Habilidad 6: Limpieza total
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo barrendero."""
        print(f"\n{C.NEGRITA}{C.VERDE}������ BARRENDERO FIL�SOFO ������{C.RESET}")
        super().mostrar_stats()
        
        # Mostrar estadísticas especiales
        print(f"\n{C.AMARILLO}������ ESTADÍSTICAS FILOS�FICAS ������{C.RESET}")
        print(f"{C.CYAN}� Calles barridas: {self._calles_barridas:3}         �{C.RESET}")
        print(f"{C.CYAN}� Reflexiones profundas: {self._reflexiones_profundas:3}   �{C.RESET}")
        print(f"{C.CYAN}� Cosas encontradas: {self._cosas_encontradas:3}       �{C.RESET}")
        print(f"{C.CYAN}� Consejos dados: {self._consejos_dados:3}          �{C.RESET}")
        print(f"{C.CYAN}� Nivel de sabiduría: {self._sabiduria:3}        �{C.RESET}")
        print(f"{C.AMARILLO}��������������������������������������{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """Recibir daño con modificadores especiales para Barrendero."""
        # El desprecio duele más
        if tipo_dano == "desprecio":
            dano = int(dano * 2.0)
            print(f"{C.ROJO_BRILLANTE}¡EL DESPRECIO DUELE! +100% daño{C.RESET}")
            
            # Pierde sabiduría
            self._sabiduria = max(0, self._sabiduria - 15)
        
        # La ignorancia lo frustra
        elif tipo_dano == "ignorancia":
            dano = int(dano * 1.6)
            print(f"{C.ROJO}¡La ignorancia duele! +60% daño{C.RESET}")
        
        # Inmune a la suciedad y el tedio
        elif tipo_dano in ["suciedad", "tedio", "monotonia"]:
            print(f"{C.AZUL}¡Acostumbrado a {tipo_dano}! Inmune.{C.RESET}")
            return 0
        
        # La sabiduría lo protege
        proteccion_sabiduria = self._sabiduria / 200  # Hasta 50% de reducción
        dano = int(dano * (1 - proteccion_sabiduria))
        
        return super().recibir_dano(dano, tipo_dano, critico)
    
    def regenerar(self):
        """Regeneración del barrendero."""
        super().regenerar()
        
        # Barre una calle (30%)
        if random.random() < 0.3:
            self._calles_barridas += 1
            
            # Encuentra algo (40%)
            if random.random() < 0.4:
                self._cosas_encontradas += 1
                hallazgo = random.choice(self._hallazgos)
                
                # Beneficio por hallazgo
                beneficio = random.choice(["vida", "energia", "sabiduria"])
                if beneficio == "vida":
                    self.vida_actual = min(self.vida_maxima, self.vida_actual + 15)
                    print(f"{C.VERDE}¡Encuentra {hallazgo} y se cura 15!{C.RESET}")
                elif beneficio == "energia":
                    self.energia_actual = min(self.energia_maxima, self.energia_actual + 20)
                    print(f"{C.AZUL}¡Encuentra {hallazgo} y recupera 20 energía!{C.RESET}")
                else:
                    self._sabiduria = min(150, self._sabiduria + 10)
                    print(f"{C.CYAN}¡Encuentra {hallazgo} y gana 10 sabiduría!{C.RESET}")
            
            print(f"{C.CYAN}» Barre una calle. Calles: {self._calles_barridas}{C.RESET}")
        
        # Reflexiona (25%)
        if random.random() < 0.25:
            self._reflexiones_profundas += 1
            reflexion = random.choice(self._reflexiones)
            
            # Gana sabiduría
            self._sabiduria = min(150, self._sabiduria + 8)
            
            print(f"{C.MAGENTA}Reflexiona {reflexion}. Sabiduría +8. Reflexiones: {self._reflexiones_profundas}{C.RESET}")
    
    def dar_consejo(self):
        """Da un consejo sabio."""
        self._consejos_dados += 1
        
        consejos = [
            "A veces hay que soltar para avanzar",
            "La paciencia es la madre de la ciencia",
            "No juzgues un libro por su portada",
            "Lo importante es el viaje, no el destino",
            "Cada día es una nueva oportunidad",
            "La verdadera riqueza está dentro",
            "Aprende de los errores, pero no te detengas en ellos",
            "La simplicidad es la mayor sofisticación"
        ]
        
        consejo = random.choice(consejos)
        
        # Beneficios del consejo
        self.vida_actual = min(self.vida_maxima, self.vida_actual + 10)
        self._sabiduria = min(150, self._sabiduria + 5)
        
        print(f"{C.VERDE}Consejo: \"{consejo}\". Vida +10, Sabiduría +5. Consejos: {self._consejos_dados}{C.RESET}")
    
    def meditar(self):
        """Medita en la calle."""
        # Gran beneficio pero toma tiempo
        self.vida_actual = min(self.vida_maxima, self.vida_actual + 25)
        self.energia_actual = min(self.energia_maxima, self.energia_actual + 30)
        self._sabiduria = min(150, self._sabiduria + 15)
        
        # Posible iluminación (5%)
        if random.random() < 0.05:
            self.estados.append("iluminado")
            print(f"{C.VERDE_BRILLANTE}¡ILUMINACI�N! Estado: iluminado{C.RESET}")
        
        print(f"{C.CYAN}¡Meditación callejera! Vida +25, Energía +30, Sabiduría +15{C.RESET}")