"""
Guiri Turista - Pobre turista que no sabe ni dónde está ni qué hace aquí
Víctima eterna de todos, pero con suerte inesperada

Estadísticas:
- Vida: 60
- Ataque: 10
- Defensa: 3
- Velocidad: 40
- Energía: 80
"""

from .personaje_base import Personaje
from habilidades.habilidades_turista import (
    PedirDirecciones,
    FotoTuristica,
    ComprarSouvenir,
    Perderse,
    HablarInglesAlto,
    BuscarWifi
)
from utils import Colores as C
import random

class Turista(Personaje):
    """
    Personaje: Guiri Turista
    Pobre turista que no sabe ni dónde está ni qué hace aquí.
    Víctima eterna pero con suerte inesperada.
    """
    
    def __init__(self, nombre_personalizado: str = None):
        super().__init__(
            nombre=nombre_personalizado if nombre_personalizado else "Hans el Alemán Perdido",
            tipo="🧳 Guiri Turista",
            vida_base=60,
            ataque_base=10,
            defensa_base=3,
            velocidad_base=40,
            energia_base=80
        )
        
        # Sistema de tipos y efectividades
        self.debilidades = ["callejero", "astucia", "estafa", "timador"]
        self.fortalezas = ["suerte", "torpeza", "ignorancia"]  # La torpeza a veces ayuda
        self.inmunidades = ["vergüenza", "idioma"]  # No entiende el idioma, no tiene vergüenza
        
        # Estadísticas especiales del turista
        self._dinero_gastado = 0
        self._fotos_tomadas = 0
        self._veces_perdido = 0
        self._souvenirs_inutiles = 0
        self._suerte = 0.1  # 10% de suerte base
        
        # Frases típicas de turista
        self._frases_turista = [
            "¿Dónde está la Sagrada Familia?",
            "¡Muy bonito!",
            "¿Habla inglés?",
            "¡Qué calor!",
            "¿Cuánto cuesta?",
            "¡Olé!",
            "¿Paella?",
            "¡Flamenco!"
        ]
        
        # Lista de cosas inútiles que compra
        self._souvenirs = [
            "imán de nevera feo",
            "pañuelo con toros",
            "abanico roto",
            "figura de flamenco",
            "llavero de la Alhambra",
            "camiseta 'I ❤️ Spain'",
            "gorra de torero",
            "castañuelas de plástico"
        ]
        
        # Inicializar habilidades
        self.inicializar_habilidades()
    
    @classmethod
    def descripcion(cls):
        return ("Pobre turista que no sabe ni dónde está ni qué hace aquí. "
                "Víctima eterna de estafas y situaciones absurdas. "
                "Débil contra casi todo, pero tiene suerte inesperada.")
    
    def inicializar_habilidades(self):
        """Inicializa las 6 habilidades únicas del Turista."""
        self.habilidades = [
            PedirDirecciones(),     # Habilidad 1: Pide ayuda
            FotoTuristica(),        # Habilidad 2: Hace fotos
            ComprarSouvenir(),      # Habilidad 3: Compra cosas inútiles
            Perderse(),             # Habilidad 4: Se pierde
            HablarInglesAlto(),     # Habilidad 5: Habla inglés fuerte
            BuscarWifi()            # Habilidad 6: Busca wifi desesperadamente
        ]
    
    def mostrar_stats(self):
        """Muestra estadísticas con estilo turista."""
        print(f"\n{C.NEGRITA}{C.AZUL}┌───── GUIRI TURISTA ─────┐{C.RESET}")
        super().mostrar_stats()
        
        # Mostrar estadísticas especiales
        print(f"\n{C.AMARILLO}┌───── ESTADÍSTICAS TURÍSTICAS ─────┐{C.RESET}")
        print(f"{C.CYAN}│ Dinero gastado: {self._dinero_gastado:5}€           │{C.RESET}")
        print(f"{C.CYAN}│ Fotos tomadas: {self._fotos_tomadas:3}                │{C.RESET}")
        print(f"{C.CYAN}│ Veces perdido: {self._veces_perdido:3}                │{C.RESET}")
        print(f"{C.CYAN}│ Souvenirs: {self._souvenirs_inutiles:3}                │{C.RESET}")
        print(f"{C.CYAN}│ Suerte: {self._suerte*100:3.0f}%                  │{C.RESET}")
        print(f"{C.AMARILLO}└──────────────────────────────────┘{C.RESET}")
    
    def recibir_dano(self, dano: int, tipo_dano: str = "normal", critico: bool = False) -> int:
        """Recibir daño con modificadores especiales para Turista."""
        # A veces la ignorancia lo salva (20% de reducir daño)
        if random.random() < 0.2:
            dano = dano // 2
            print(f"{C.VERDE}¡No se entera de nada! Mitad de daño.{C.RESET}")
        
        # Suerte inesperada (10% base de esquivar)
        if random.random() < self._suerte:
            print(f"{C.VERDE_BRILLANTE}¡Suerte del principiante! Esquiva el ataque.{C.RESET}")
            return 0
        
        # Aumentar suerte por cada golpe recibido
        self._suerte = min(0.5, self._suerte + 0.01)
        
        return super().recibir_dano(dano, tipo_dano, critico)
    
    def regenerar(self):
        """Regeneración turística."""
        super().regenerar()
        
        # Los turistas encuentran monedas en el suelo (15%)
        if random.random() < 0.15:
            monedas = random.randint(1, 10)
            self._dinero_gastado -= monedas  # "Encuentra" dinero
            print(f"{C.AMARILLO}¡Encuentra {monedas}€ en el suelo!{C.RESET}")
        
        # Toma fotos aleatorias (20%)
        if random.random() < 0.2:
            self._fotos_tomadas += 1
            sujetos = ["un gato", "una farola", "su propio pie", "algo que no sabe qué es"]
            sujeto = random.choice(sujetos)
            print(f"{C.CYAN}» {self.nombre} fotografía {sujeto}. Fotos: {self._fotos_tomadas}{C.RESET}")
    
    def comprar_souvenir(self):
        """Compra un souvenir inútil."""
        souvenir = random.choice(self._souvenirs)
        costo = random.randint(5, 20)
        self._dinero_gastado += costo
        self._souvenirs_inutiles += 1
        
        print(f"{C.MAGENTA}¡Compra un {souvenir} por {costo}€! Total gastado: {self._dinero_gastado}€{C.RESET}")
        return souvenir
    
    def perderse(self):
        """Se pierde (de nuevo)."""
        self._veces_perdido += 1
        lugares = ["en una calle sin salida", "en el metro", "en un museo", "en su propio hotel"]
        lugar = random.choice(lugares)
        
        print(f"{C.ROJO}¡Se pierde {lugar} por {self._veces_perdido}ª vez!{C.RESET}")
        
        # A veces encuentra algo útil (30%)
        if random.random() < 0.3:
            hallazgos = ["un mapa", "una señal", "un policía amable", "un wifi abierto"]
            hallazgo = random.choice(hallazgos)
            print(f"{C.VERDE}Pero encuentra {hallazgo}.{C.RESET}")
            
            if hallazgo == "un wifi abierto":
                self.energia_actual = min(self.energia_maxima, self.energia_actual + 20)