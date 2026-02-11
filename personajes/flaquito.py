"""
Flaquito Playero - El típico flaco que va a la playa y no se pone moreno
Especialista en esquivar y sobrevivir con suerte

Estadísticas:
- Vida: 55
- Ataque: 8
- Defensa: 2
- Velocidad: 75
- Energía: 85
"""

from .personaje_base import Personaje
from habilidades.habilidades_flaquito import (
    ArenaEnLosOjos,
    SurfearOla,
    BronceadoExpress,
    Esquivel,
    PalizaDeToalla,
    RefrescoAzucarado
)
from utils import Colores as C
import random

class Flaquito(Personaje):
    """
    Personaje: Flaquito Playero
    El típico flaco que va a la playa y no se pone moreno.
    Especialista en esquivar y sobrevivir con suerte.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Julián el Desnutrido",
            tipo="🏖️ Flaquito Playero",
            vida_base=55,
            ataque_base=8,
            defensa_base=2,
            velocidad_base=75,
            energia_base=85
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["comida", "viento", "sol", "fuerza"]
        self.fortalezas = ["agilidad", "sigilo", "suerte", "evasion"]
        self.inmunidades = ["complejo", "vergüenza"]  # No tiene complejos
        
        # Estadísticas especiales del flaquito
        self._veces_volado = 0
        self._quemaduras_solares = 0
        self._refrescos_bebidos = 0
        self._olas_surfeadas = 0
        self._suerte = 0.25  # 25% de suerte base
        
        # Frases típicas de flaquito
        self._frases_flaquito = [
            "¡Me voy a volar!",
            "¿Tienes protector solar?",
            "¡Qué fuerte el viento!",
            "Necesito un refresco",
            "¿A qué hora es la siesta?",
            "¡Casi me caigo!",
            "Tengo hambre",
            "¡Otra ola!"
        ]
        
        # Cosas que pierde con el viento
        self._cosas_perdidas = [
            "la toalla",
            "las chanclas",
            "la gorra",
            "las gafas de sol",
            "el móvil",
            "la crema solar",
            "el dinero",
            "las llaves"
        ]
        
        # Inicializar habilidades
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("El típico flaco que va a la playa y no se pone moreno. "
                "Especialista en esquivar y sobrevivir con suerte. "
                "Extremadamente ágil pero muy frágil.")
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas del Flaquito."""
        self.habilidades = [
            ArenaEnLosOjos(),     # Habilidad 1: Lanza arena
            SurfearOla(),         # Habilidad 2: Surfea una ola
            BronceadoExpress(),   # Habilidad 3: Se pone moreno
            Esquivel(),           # Habilidad 4: Esquiva ataques
            PalizaDeToalla(),     # Habilidad 5: Golpea con toalla
            RefrescoAzucarado()   # Habilidad 6: Bebe refresco
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo flaquito."""
        print(f"\n{C.NEGRITA}{C.AMARILLO}┌───── FLAQUITO PLAYERO ─────┐{C.RESET}")
        super().mostrar_stats()
        
        # Mostrar estadísticas especiales
        print(f"\n{C.AMARILLO}┌───── ESTADÍSTICAS PLAYERAS ─────┐{C.RESET}")
        print(f"{C.CYAN}│ Veces volado: {self._veces_volado:3}            │{C.RESET}")
        print(f"{C.CYAN}│ Quemaduras solares: {self._quemaduras_solares:3}     │{C.RESET}")
        print(f"{C.CYAN}│ Refrescos bebidos: {self._refrescos_bebidos:3}      │{C.RESET}")
        print(f"{C.CYAN}│ Olas surfeadas: {self._olas_surfeadas:3}         │{C.RESET}")
        print(f"{C.CYAN}│ Suerte: {self._suerte*100:3.0f}%               │{C.RESET}")
        print(f"{C.AMARILLO}└──────────────────────────────────┘{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """Recibir daño con modificadores especiales para Flaquito."""
        # El viento lo vuela (daño extra)
        if tipo_dano == "viento":
            dano = int(dano * 1.8)
            self._veces_volado += 1
            
            # Pierde algo (40%)
            if random.random() < 0.4:
                cosa_perdida = random.choice(self._cosas_perdidas)
                print(f"{C.ROJO}¡Se lo lleva el viento! Pierde {cosa_perdida}. +80% daño{C.RESET}")
            else:
                print(f"{C.ROJO}¡Casi se vuela! +80% daño{C.RESET}")
        
        # El sol lo quema
        elif tipo_dano == "sol":
            dano = int(dano * 1.5)
            self._quemaduras_solares += 1
            print(f"{C.ROJO}¡Quemadura solar! +50% daño. Total: {self._quemaduras_solares}{C.RESET}")
            
            # Posible estado: quemado
            if random.random() < 0.3:
                self.estados.append("quemado")
                print(f"{C.MAGENTA}¡Le duele al moverse! Estado: quemado{C.RESET}")
        
        # Suerte para esquivar (25% base)
        elif random.random() < self._suerte:
            print(f"{C.VERDE_BRILLANTE}¡Suerte del flaco! Esquiva milagrosamente.{C.RESET}")
            return 0
        
        # Aumenta suerte por cada golpe recibido
        self._suerte = min(0.5, self._suerte + 0.02)
        
        return super().recibir_dano(dano, tipo_dano, critico)
    
    def regenerar(self):
        """Regeneración del flaquito."""
        super().regenerar()
        
        # Bebe un refresco (30%)
        if random.random() < 0.3:
            self._refrescos_bebidos += 1
            
            # Beneficios del refresco
            azucar_extra = random.randint(5, 15)
            self.energia_actual = min(self.energia_maxima, self.energia_actual + azucar_extra)
            
            print(f"{C.CYAN}» Bebe un refresco. Energía +{azucar_extra}. Total: {self._refrescos_bebidos}{C.RESET}")
        
        # Se aplica crema solar (20%)
        if random.random() < 0.2 and self._quemaduras_solares > 0:
            crema_efectiva = min(3, self._quemaduras_solares)
            self._quemaduras_solares -= crema_efectiva
            
            # Cura un poco
            curacion_crema = crema_efectiva * 5
            self.vida_actual = min(self.vida_maxima, self.vida_actual + curacion_crema)
            
            print(f"{C.VERDE}¡Crema solar! Quemaduras -{crema_efectiva}, Vida +{curacion_crema}.{C.RESET}")
    
    def surfear_ola(self):
        """Surfea una ola."""
        self._olas_surfeadas += 1
        
        # Beneficios por surfear
        self.velocidad += 5
        self._suerte = min(0.5, self._suerte + 0.05)
        
        print(f"{C.AZUL}¡Surfea una ola! Velocidad +5, Suerte +5%. Total: {self._olas_surfeadas}{C.RESET}")
    
    def volar_con_viento(self):
        """El viento lo vuela (de nuevo)."""
        self._veces_volado += 1
        destino = random.choice(["la sombrilla", "el chiringuito", "el agua", "otra playa"])
        
        print(f"{C.ROJO}¡Se vuela hasta {destino}! Veces volado: {self._veces_volado}{C.RESET}")
        
        # A veces encuentra algo (20%)
        if random.random() < 0.2:
            hallazgos = ["una moneda", "una concha bonita", "una pelota", "un amigo"]
            hallazgo = random.choice(hallazgos)
            print(f"{C.VERDE}Pero encuentra {hallazgo}.{C.RESET}")