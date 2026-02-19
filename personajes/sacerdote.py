"""
Super Sacerdote - Un cura con más poder que un superhéroe de Marvel
Especializado en exorcismos y bendiciones

Estadísticas:
- Vida: 115
- Ataque: 16
- Defensa: 16
- Velocidad: 55
- Energía: 120
"""

from .personaje_base import Personaje
from habilidades.habilidades_sacerdote import (
    Exorcismo,
    BendicionDivina,
    AguaBenditaAvanzada,
    SermonEterno,
    MilagroDivino,
    CastigoDivino
)
from utils import Colores as C
import random

class Sacerdote(Personaje):
    """
    Personaje: Super Sacerdote
    Un cura con más poder que un superhéroe de Marvel.
    Especializado en exorcismos, bendiciones y milagros.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Padre Benito",
            tipo="�️ Super Sacerdote",
            vida_base=115,
            ataque_base=16,
            defensa_base=16,
            velocidad_base=55,
            energia_base=120
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["politico", "herejia", "ateismo"]
        self.fortalezas = ["religioso", "espiritual", "divino"]
        self.inmunidades = ["pecado", "tentacion", "posesion"]
        
        # Estadísticas especiales del sacerdote
        self._fe_acumulada = 200
        self._fe_maxima = 300
        self._exorcismos_realizados = 0
        self._milagros_realizados = 0
        self._sacramentos = ["bautismo", "comunión", "confirmación", "confesión"]
        
        # Frases sagradas
        self._frases_sagradas = [
            "¡En el nombre del Padre, del Hijo y del Espíritu Santo!",
            "¡Vade retro, Satanás!",
            "¡El Señor es mi pastor, nada me falta!",
            "¡Dios te ve, hijo mío!",
            "¡Confiesa tus pecados!",
            "¡Recibe la gracia divina!"
        ]
        
        # Inicializar habilidades
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("Un cura con más poder que un superhéroe de Marvel. "
                "Especializado en exorcismos, bendiciones y milagros. "
                "Tremendamente poderoso contra demonios y pecadores.")
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas del Sacerdote."""
        self.habilidades = [
            Exorcismo(),           # Habilidad 1: Exorciza demonios
            BendicionDivina(),     # Habilidad 2: Bendice y cura
            AguaBenditaAvanzada(), # Habilidad 3: Agua bendita potenciada
            SermonEterno(),        # Habilidad 4: Sermón eterno
            MilagroDivino(),       # Habilidad 5: Realiza un milagro
            CastigoDivino()        # Habilidad 6: Castigo de Dios
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo sacerdote."""
        print(f"\n{C.NEGRITA}{C.CYAN}������ SUPER SACERDOTE ������{C.RESET}")
        super().mostrar_stats()
        
        # Mostrar estadísticas especiales
        print(f"\n{C.AMARILLO}������ ESTADÍSTICAS DIVINAS ������{C.RESET}")
        print(f"{C.CYAN}� Fe acumulada: {self._fe_acumulada:4}/{self._fe_maxima:<4}          �{C.RESET}")
        print(f"{C.CYAN}� Exorcismos: {self._exorcismos_realizados:3}                   �{C.RESET}")
        print(f"{C.CYAN}� Milagros: {self._milagros_realizados:3}                     �{C.RESET}")
        print(f"{C.CYAN}� Sacramentos: {len(self._sacramentos)}/4               �{C.RESET}")
        print(f"{C.AMARILLO}�����������������������������������{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """Recibir daño con modificadores especiales para Sacerdote."""
        # Inmune a posesiones y pecados
        if tipo_dano in ["posesion", "pecado", "demonio"]:
            print(f"{C.AZUL}¡La fe lo protege! Inmune a {tipo_dano}.{C.RESET}")
            return 0
        
        # Resistencia divina
        if tipo_dano in ["espiritual", "divino", "religioso"]:
            dano = dano // 2
            print(f"{C.VERDE}¡Bendición divina! Resistencia a {tipo_dano}.{C.RESET}")
        
        # Vulnerable a herejías
        if tipo_dano in ["herejia", "ateismo", "blasfemia"]:
            dano = int(dano * 1.8)
            print(f"{C.ROJO}¡Herejía! Le duele en el alma. +80% daño{C.RESET}")
            
            # Posible pérdida de fe
            if random.random() < 0.3:
                fe_perdida = random.randint(10, 30)
                self._fe_acumulada = max(0, self._fe_acumulada - fe_perdida)
                print(f"{C.ROJO}¡Pierde {fe_perdida} de fe por la herejía!{C.RESET}")
        
        return super().recibir_dano(dano, tipo_dano, critico)
    
    def regenerar(self):
        """Regeneración divina del Sacerdote."""
        super().regenerar()
        
        # Regeneración de fe por oración
        fe_regenerada = random.randint(10, 25)
        self._fe_acumulada = min(self._fe_maxima, self._fe_acumulada + fe_regenerada)
        
        # Sanación divina ocasional (20%)
        if random.random() < 0.2 and self.vida_actual < self.vida_maxima * 0.7:
            curacion_divina = max(10, self.vida_maxima // 8)
            self.vida_actual = min(self.vida_maxima, self.vida_actual + curacion_divina)
            print(f"{C.VERDE}¡Gracia divina! Se cura {curacion_divina} puntos.{C.RESET}")
        
        # Frase sagrada ocasional (25%)
        if random.random() < 0.25:
            frase = random.choice(self._frases_sagradas)
            print(f"{C.CYAN}» {self.nombre}: \"{frase}\"{C.RESET}")