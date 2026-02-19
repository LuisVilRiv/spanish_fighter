"""
Choni de Barrio - Choni con uñas de 2 metros y mucho carácter
Especialista en chismes, selfies y actitud

Estadísticas:
- Vida: 95
- Ataque: 26
- Defensa: 10
- Velocidad: 70
- Energía: 100
"""

from .personaje_base import Personaje
from habilidades.habilidades_choni import (
    TacónEnElPie,
    MiradaDeHielo,
    SelfieConFiltro,
    Uñazo,
    Chismorreo,
    FiestaDelPueblo
)
from utils import Colores as C
import random

class Choni(Personaje):
    """
    Personaje: Choni de Barrio
    Choni con uñas de 2 metros y mucho carácter.
    Especialista en chismes, selfies y actitud.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Yenni",
            tipo="� Choni de Barrio",
            vida_base=95,
            ataque_base=26,
            defensa_base=10,
            velocidad_base=70,
            energia_base=100
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["educacion", "clase", "elegancia", "cultura"]
        self.fortalezas = ["calle", "atrevimiento", "chisme", "actitud"]
        self.inmunidades = ["vergüenza", "critica"]  # No siente vergüenza
        
        # Estadísticas especiales de la choni
        self._selfies_tomadas = 0
        self._chismes_contados = 0
        self._uñas_rotas = 0
        self._fiestas_asistidas = 0
        self._actitud = 100  # Nivel de actitud (0-100)
        
        # Frases típicas de choni
        self._frases_choni = [
            "¡Qué pasó, tronca!",
            "¡No me toques las uñas!",
            "¡Vamos de fiesta!",
            "¡Te voy a contar un chisme!",
            "¡Qué fuerte!",
            "¡Me piro!",
            "¡Está guapísimo!",
            "¡Lo vi en FotoFeed!"
        ]
        
        # Filtros de FotoFeed
        self._filtros = [
            "perrito",
            "corazones",
            "flores",
            "arcoíris",
            "estrellas",
            "mariposas",
            "glitter",
            "corona"
        ]
        
        # Chismes típicos
        self._chismes = [
            "María se fue con Juan",
            "Pedro engaña a Laura",
            "Ana se operó la nariz",
            "Luis debe dinero",
            "Carla se tatuó el nombre de su ex",
            "Pablo fue a la cárcel",
            "Sofía se hizo botox",
            "Javier tiene un hijo secreto"
        ]
        
        # Inicializar habilidades
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("Choni con uñas de 2 metros y mucho carácter. "
                "Especialista en chismes, selfies y actitud. "
                "Nada la avergüenza, pero la educación la derrota.")
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas de la Choni."""
        self.habilidades = [
            TacónEnElPie(),      # Habilidad 1: Golpe con tacón
            MiradaDeHielo(),     # Habilidad 2: Mirada paralizante
            SelfieConFiltro(),   # Habilidad 3: Selfie con filtro
            Uñazo(),             # Habilidad 4: Arañazo con uñas
            Chismorreo(),        # Habilidad 5: Cuenta un chisme
            FiestaDelPueblo()    # Habilidad 6: Va de fiesta
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo choni."""
        print(f"\n{C.NEGRITA}{C.MAGENTA}������ CHONI DE BARRIO ������{C.RESET}")
        super().mostrar_stats()
        
        # Mostrar estadísticas especiales
        print(f"\n{C.AMARILLO}������ ESTADÍSTICAS CHONIS ������{C.RESET}")
        print(f"{C.CYAN}� Selfies tomadas: {self._selfies_tomadas:3}        �{C.RESET}")
        print(f"{C.CYAN}� Chismes contados: {self._chismes_contados:3}       �{C.RESET}")
        print(f"{C.CYAN}� Uñas rotas: {self._uñas_rotas:3}             �{C.RESET}")
        print(f"{C.CYAN}� Fiestas asistidas: {self._fiestas_asistidas:3}     �{C.RESET}")
        print(f"{C.CYAN}� Nivel de actitud: {self._actitud:3}          �{C.RESET}")
        print(f"{C.AMARILLO}����������������������������������{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """Recibir daño con modificadores especiales para Choni."""
        # La educación la destruye
        if tipo_dano == "educacion":
            dano = int(dano * 2.0)
            print(f"{C.ROJO_BRILLANTE}¡LA EDUCACI�N LA MATA! +100% daño{C.RESET}")
            
            # Pierde actitud
            self._actitud = max(0, self._actitud - 20)
        
        # Inmune a la vergüenza
        elif tipo_dano == "vergüenza":
            print(f"{C.AZUL}¡No sabe lo que es la vergüenza! Inmune.{C.RESET}")
            return 0
        
        # Las uñas se rompen (20% si es daño físico)
        elif tipo_dano == "fisico" and random.random() < 0.2:
            self._uñas_rotas += 1
            print(f"{C.ROJO}¡Se le rompe una uña! Uñas rotas: {self._uñas_rotas}{C.RESET}")
            
            # Pierde ataque temporalmente
            self.ataque = max(5, self.ataque - 3)
        
        return super().recibir_dano(dano, tipo_dano, critico)
    
    def regenerar(self):
        """Regeneración de la choni."""
        super().regenerar()
        
        # Se toma un selfie (35%)
        if random.random() < 0.35:
            self._selfies_tomadas += 1
            filtro = random.choice(self._filtros)
            
            # Sube actitud con selfies
            self._actitud = min(100, self._actitud + 10)
            
            print(f"{C.MAGENTA}¡Selfie con filtro de {filtro}! Actitud +10. Selfies: {self._selfies_tomadas}{C.RESET}")
        
        # Cuenta un chisme (25%)
        if random.random() < 0.25:
            self._chismes_contados += 1
            chisme = random.choice(self._chismes)
            
            # Beneficio por chisme
            self.energia_actual = min(self.energia_maxima, self.energia_actual + 15)
            
            print(f"{C.CYAN}» Cuenta: \"{chisme}\". Energía +15. Chismes: {self._chismes_contados}{C.RESET}")
    
    def ir_de_fiesta(self):
        """Va de fiesta."""
        self._fiestas_asistidas += 1
        
        # Grandes beneficios pero posibles consecuencias
        self.vida_actual = min(self.vida_maxima, self.vida_actual + 25)
        self.energia_actual = min(self.energia_maxima, self.energia_actual + 40)
        self._actitud = min(100, self._actitud + 30)
        
        # Posible resaca (10%)
        if random.random() < 0.1:
            self.estados.append("resaca")
            print(f"{C.ROJO}¡Resaca! Pero valió la pena.{C.RESET}")
        
        print(f"{C.VERDE_BRILLANTE}¡Fiesta! Vida +25, Energía +40, Actitud +30. Total: {self._fiestas_asistidas}{C.RESET}")
    
    def arreglar_unas(self):
        """Se arregla las uñas."""
        if self._uñas_rotas > 0:
            self._uñas_rotas = 0
            self.ataque += 5  # Uñas nuevas, más peligro
            
            print(f"{C.MAGENTA}¡Uñas arregladas! Ataque +5.{C.RESET}")