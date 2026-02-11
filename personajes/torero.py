"""
El Fatal Torero - Torero con más arte que un museo
Maestro de la lidia y el valor temerario

Estadísticas:
- Vida: 85
- Ataque: 22
- Defensa: 7
- Velocidad: 70
- Energía: 105
"""

from .personaje_base import Personaje
from habilidades.habilidades_torero import (
    PaseDeTorero,
    Estocada,
    OlesDelPublico,
    Capote,
    Finta,
    Faena
)
from utils import Colores as C
import random

class Torero(Personaje):
    """
    Personaje: El Fatal Torero
    Torero con más arte que un museo.
    Maestro de la lidia y el valor temerario.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "El Fatal",
            tipo="🐂 El Fatal Torero",
            vida_base=85,
            ataque_base=22,
            defensa_base=7,
            velocidad_base=70,
            energia_base=105
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["animalista", "miedo", "cornada", "peta"]
        self.fortalezas = ["arte", "tradicion", "valor", "elegancia"]
        self.inmunidades = ["vergüenza", "temor"]  # No siente vergüenza ni miedo
        
        # Estadísticas especiales del torero
        self._orejas_conseguidas = 0
        self._cornadas_recibidas = 0
        self._faenas_completas = 0
        self._publico_entusiasmado = 0
        self._arte = 100  # Nivel artístico (0-100)
        
        # Frases típicas de torero
        self._frases_torero = [
            "¡Olé!",
            "¡Toro!",
            "¡Qué arte!",
            "¡Toma ya!",
            "¡Viva el toro!",
            "¡Esto es arte!",
            "¡Al toro!",
            "¡A estoquear!"
        ]
        
        # Pases de torero
        self._pases = [
            "de pecho",
            "de rodillas",
            "de muleta",
            "natural",
            "de castigo",
            "de frente",
            "por detrás",
            "de fantasía"
        ]
        
        # Inicializar habilidades
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("Torero con más arte que un museo. "
                "Maestro de la lidia y el valor temerario. "
                "Elegante y arriesgado, pero vulnerable a las cornadas.")
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas del Torero."""
        self.habilidades = [
            PaseDeTorero(),   # Habilidad 1: Pase artístico
            Estocada(),       # Habilidad 2: Estocada final
            OlesDelPublico(), # Habilidad 3: Olés del público
            Capote(),         # Habilidad 4: Defensa con capote
            Finta(),          # Habilidad 5: Finta engañosa
            Faena()           # Habilidad 6: Faena completa
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo torero."""
        print(f"\n{C.NEGRITA}{C.ROJO}┌───── EL FATAL TORERO ─────┐{C.RESET}")
        super().mostrar_stats()
        
        # Mostrar estadísticas especiales
        print(f"\n{C.AMARILLO}┌───── ESTADÍSTICAS TAUROMÁQUICAS ─────┐{C.RESET}")
        print(f"{C.CYAN}│ Orejas conseguidas: {self._orejas_conseguidas:3}       │{C.RESET}")
        print(f"{C.CYAN}│ Cornadas recibidas: {self._cornadas_recibidas:3}       │{C.RESET}")
        print(f"{C.CYAN}│ Faenas completas: {self._faenas_completas:3}        │{C.RESET}")
        print(f"{C.CYAN}│ Público entusiasmado: {self._publico_entusiasmado:3}   │{C.RESET}")
        print(f"{C.CYAN}│ Nivel de arte: {self._arte:3}              │{C.RESET}")
        print(f"{C.AMARILLO}└──────────────────────────────────────┘{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """Recibir daño con modificadores especiales para Torero."""
        # Cornadas son especialmente peligrosas
        if tipo_dano == "cornada":
            dano = int(dano * 3.0)
            self._cornadas_recibidas += 1
            print(f"{C.ROJO_BRILLANTE}¡CORNADA! x3 daño. Total: {self._cornadas_recibidas}{C.RESET}")
            
            # Posible herida grave (10%)
            if random.random() < 0.1:
                self.estados.append("herido_grave")
                print(f"{C.ROJO}¡Herida grave! Estado: herido_grave{C.RESET}")
        
        # Vulnerable a protestas animalistas
        elif tipo_dano == "animalista":
            dano = int(dano * 1.5)
            print(f"{C.ROJO}¡Protesta animalista! +50% daño{C.RESET}")
            
            # Pierde arte
            self._arte = max(0, self._arte - 10)
        
        # Resistente al miedo
        elif tipo_dano == "miedo":
            dano = dano // 3
            print(f"{C.VERDE}¡No conoce el miedo! /3 daño{C.RESET}")
        
        return super().recibir_dano(dano, tipo_dano, critico)
    
    def regenerar(self):
        """Regeneración del torero."""
        super().regenerar()
        
        # Practica pases (30%)
        if random.random() < 0.3:
            pase = random.choice(self._pases)
            self._arte = min(100, self._arte + 5)
            
            print(f"{C.CYAN}» Practica pase {pase}. Arte +5. Nivel: {self._arte}{C.RESET}")
        
        # El público lo anima (25%)
        if random.random() < 0.25 and self._publico_entusiasmado < 10:
            self._publico_entusiasmado += 1
            frase = random.choice(self._frases_torero)
            
            # Beneficios del público
            beneficios = ["+10 energía", "+5 vida", "+3 ataque", "+2 velocidad"]
            beneficio = random.choice(beneficios)
            
            if "+10 energía" in beneficio:
                self.energia_actual = min(self.energia_maxima, self.energia_actual + 10)
            elif "+5 vida" in beneficio:
                self.vida_actual = min(self.vida_maxima, self.vida_actual + 5)
            elif "+3 ataque" in beneficio:
                self.ataque += 3
            elif "+2 velocidad" in beneficio:
                self.velocidad += 2
            
            print(f"{C.VERDE}¡Público: \"{frase}\"! {beneficio}. Entusiasmo: {self._publico_entusiasmado}{C.RESET}")
    
    def conseguir_oreja(self):
        """Consigue una oreja (trofeo)."""
        self._orejas_conseguidas += 1
        
        # Beneficios por oreja
        self.vida_actual = min(self.vida_maxima, self.vida_actual + 15)
        self._arte = min(100, self._arte + 20)
        
        print(f"{C.AMARILLO}¡Oreja conseguida! Vida +15, Arte +20. Total: {self._orejas_conseguidas}{C.RESET}")
    
    def completar_faena(self):
        """Completa una faena exitosa."""
        self._faenas_completas += 1
        
        # Gran beneficio
        self.vida_actual = min(self.vida_maxima, self.vida_actual + 30)
        self.energia_actual = min(self.energia_maxima, self.energia_actual + 40)
        self._arte = min(100, self._arte + 30)
        
        print(f"{C.VERDE_BRILLANTE}¡Faena completa! Vida +30, Energía +40, Arte +30. Total: {self._faenas_completas}{C.RESET}")