"""
Político Prometedor - Político que promete cosas y no cumple ninguna
Maestro de la mentira y el discurso vacío

Estadísticas:
- Vida: 100
- Ataque: 18
- Defensa: 12
- Velocidad: 65
- Energía: 95
"""

from .personaje_base import Personaje
from habilidades.habilidades_politico import (
    DiscursoVacio,
    PromesaFalsa,
    FotoConBebe,
    DesviarAtencion,
    SubirImpuestos,
    CampanaElectoral
)
from utils import Colores as C
import random

class Politico(Personaje):
    """
    Personaje: Político Prometedor
    Político que promete cosas y no cumple ninguna.
    Maestro de la mentira y el discurso vacío.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Don Prometelo Todo",
            tipo="� Político Prometedor",
            vida_base=100,
            ataque_base=18,
            defensa_base=12,
            velocidad_base=65,
            energia_base=95
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["verdad", "transparencia", "periodismo", "pruebas"]
        self.fortalezas = ["mentira", "promesa", "demagogia", "retorica"]
        self.inmunidades = ["critica", "escandalo", "corrupcion"]  # Son inmunes
        
        # Estadísticas especiales del político
        self._promesas_incumplidas = 0
        self._discursos_vacios = 0
        self._fotos_con_bebes = 0
        self._impuestos_subidos = 0
        self._popularidad = 50  # 0-100
        
        # Frases típicas de político
        self._frases_politico = [
            "Voy a crear 500.000 empleos",
            "Es una medida temporal",
            "Lo heredé del gobierno anterior",
            "Estamos en la buena dirección",
            "Es una fake news",
            "No tengo constancia de eso",
            "Lo vamos a estudiar",
            "Es culpa de la oposición"
        ]
        
        # Promesas vacías
        self._promesas = [
            "bajar los impuestos",
            "mejorar la sanidad",
            "arreglar la educación",
            "crear empleo",
            "subir las pensiones",
            "mejorar las infraestructuras",
            "combatir la corrupción",
            "proteger el medio ambiente"
        ]
        
        # Inicializar habilidades
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("Político que promete cosas y no cumple ninguna. "
                "Maestro de la mentira y el discurso vacío. "
                "Débil contra la verdad y la transparencia.")
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas del Político."""
        self.habilidades = [
            DiscursoVacio(),      # Habilidad 1: Discurso sin contenido
            PromesaFalsa(),       # Habilidad 2: Promete algo falso
            FotoConBebe(),        # Habilidad 3: Se fotografía con un bebé
            DesviarAtencion(),    # Habilidad 4: Cambia de tema
            SubirImpuestos(),     # Habilidad 5: Sube impuestos
            CampanaElectoral()    # Habilidad 6: Campaña electoral
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo político."""
        print(f"\n{C.NEGRITA}{C.AMARILLO}������ POLÍTICO PROMETEDOR ������{C.RESET}")
        super().mostrar_stats()
        
        # Mostrar estadísticas especiales
        print(f"\n{C.AMARILLO}������ ESTADÍSTICAS POLÍTICAS ������{C.RESET}")
        print(f"{C.CYAN}� Promesas incumplidas: {self._promesas_incumplidas:3}   �{C.RESET}")
        print(f"{C.CYAN}� Discursos vacíos: {self._discursos_vacios:3}       �{C.RESET}")
        print(f"{C.CYAN}� Fotos con bebés: {self._fotos_con_bebes:3}        �{C.RESET}")
        print(f"{C.CYAN}� Impuestos subidos: {self._impuestos_subidos:3}      �{C.RESET}")
        print(f"{C.CYAN}� Popularidad: {self._popularidad:3}            �{C.RESET}")
        print(f"{C.AMARILLO}������������������������������������{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """Recibir daño con modificadores especiales para Político."""
        # Vulnerable a la verdad
        if tipo_dano == "verdad":
            dano = int(dano * 2.5)
            print(f"{C.ROJO_BRILLANTE}¡LA VERDAD DUELE! +150% daño{C.RESET}")
            
            # Pierde popularidad
            self._popularidad = max(0, self._popularidad - 10)
        
        # Inmune a críticas y escándalos
        if tipo_dano in ["critica", "escandalo", "corrupcion"]:
            print(f"{C.AZUL}¡Inmune! Ya está acostumbrado a {tipo_dano}.{C.RESET}")
            return 0
        
        # Resistencia a las mentiras (mitad de daño)
        if tipo_dano == "mentira":
            dano = dano // 2
            print(f"{C.VERDE}¡Experto en mentiras! Mitad de daño.{C.RESET}")
        
        return super().recibir_dano(dano, tipo_dano, critico)
    
    def regenerar(self):
        """Regeneración política."""
        super().regenerar()
        
        # Da un discurso vacío (25%)
        if random.random() < 0.25:
            self._discursos_vacios += 1
            frase = random.choice(self._frases_politico)
            print(f"{C.CYAN}» {self.nombre}: \"{frase}\" (Discurso {self._discursos_vacios}){C.RESET}")
            
            # Aumenta popularidad con discursos
            self._popularidad = min(100, self._popularidad + 3)
        
        # Hace una promesa falsa (20%)
        if random.random() < 0.2:
            self._promesas_incumplidas += 1
            promesa = random.choice(self._promesas)
            print(f"{C.MAGENTA}¡Promete {promesa}! Promesas incumplidas: {self._promesas_incumplidas}{C.RESET}")
    
    def tomar_foto_con_bebe(self):
        """Se toma una foto con un bebé para subir popularidad."""
        self._fotos_con_bebes += 1
        self._popularidad = min(100, self._popularidad + 5)
        
        print(f"{C.VERDE}¡Foto con bebé! Popularidad +5. Total: {self._fotos_con_bebes} fotos.{C.RESET}")
    
    def subir_impuestos(self):
        """Sube los impuestos."""
        self._impuestos_subidos += 1
        
        # Pierde popularidad pero gana energía (dinero)
        self._popularidad = max(0, self._popularidad - 15)
        self.energia_actual = min(self.energia_maxima, self.energia_actual + 30)
        
        print(f"{C.ROJO}¡Sube impuestos! Energía +30, Popularidad -15.{C.RESET}")